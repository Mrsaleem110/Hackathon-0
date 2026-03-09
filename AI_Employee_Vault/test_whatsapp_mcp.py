"""
Test WhatsApp MCP Server
"""

import json
import subprocess
import sys
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def test_whatsapp_mcp():
    """Test WhatsApp MCP Server"""

    print("="*60)
    print("Testing WhatsApp MCP Server")
    print("="*60)

    # Start server
    server_path = Path("whatsapp_mcp_server.py")
    process = subprocess.Popen(
        [sys.executable, str(server_path)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    tests = [
        {
            "name": "List Tools",
            "request": {"method": "tools/list"}
        },
        {
            "name": "Create WhatsApp Task",
            "request": {
                "method": "tools/call",
                "params": {
                    "name": "create_whatsapp_task",
                    "arguments": {
                        "sender": "Client A",
                        "message": "Urgent: Need invoice #1234 ASAP for records",
                        "priority": "high"
                    }
                }
            }
        },
        {
            "name": "List WhatsApp Tasks",
            "request": {
                "method": "tools/call",
                "params": {
                    "name": "list_whatsapp_tasks",
                    "arguments": {}
                }
            }
        },
        {
            "name": "Draft Reply",
            "request": {
                "method": "tools/call",
                "params": {
                    "name": "send_whatsapp_reply",
                    "arguments": {
                        "recipient": "Client A",
                        "message": "Hi! I'll send invoice #1234 right away. Thanks for your patience!"
                    }
                }
            }
        }
    ]

    results = []

    for test in tests:
        print(f"\n{'='*60}")
        print(f"Test: {test['name']}")
        print(f"{'='*60}")

        # Send request
        request_json = json.dumps(test['request']) + "\n"
        process.stdin.write(request_json)
        process.stdin.flush()

        # Get response
        response_line = process.stdout.readline()

        try:
            response = json.loads(response_line)

            if "error" in response:
                print(f"❌ FAIL: {response['error']}")
                results.append(False)
            else:
                print(f"✅ PASS")
                if "tools" in response:
                    print(f"   Found {len(response['tools'])} tools")
                elif "content" in response:
                    for content in response['content']:
                        print(f"   {content.get('text', '')}")
                results.append(True)

        except Exception as e:
            print(f"❌ FAIL: {e}")
            results.append(False)

    # Cleanup
    process.terminate()
    process.wait()

    # Summary
    print(f"\n{'='*60}")
    print("Test Summary")
    print(f"{'='*60}")
    print(f"Total: {len(results)}")
    print(f"Passed: {sum(results)}")
    print(f"Failed: {len(results) - sum(results)}")

    if all(results):
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed")

    return all(results)


if __name__ == "__main__":
    success = test_whatsapp_mcp()
    sys.exit(0 if success else 1)
