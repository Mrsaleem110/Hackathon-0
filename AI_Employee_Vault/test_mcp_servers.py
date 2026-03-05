"""
MCP Server Integration Test
Tests both Email and Vault MCP servers
"""

import json
import sys
from pathlib import Path

# Add MCP to path
sys.path.insert(0, str(Path(__file__).parent / 'MCP'))

from email_mcp_server import MCPServer as EmailMCPServer
from vault_mcp_server import MCPVaultServer

def test_email_mcp():
    """Test Email MCP Server"""
    print("\n" + "="*60)
    print("Testing Email MCP Server")
    print("="*60)

    server = EmailMCPServer(vault_path=".")

    # Show capabilities
    print("\nEmail MCP Capabilities:")
    caps = server.get_capabilities()
    print(json.dumps(caps, indent=2))

    # Test send_email request
    print("\nTesting send_email request:")
    request = {
        'service': 'email',
        'method': 'send_email',
        'params': {
            'to': 'client@example.com',
            'subject': 'Test Email from MCP',
            'body': 'This is a test email from the MCP server.'
        }
    }
    result = server.process_request(request)
    print(json.dumps(result, indent=2))

    # Test draft_email request
    print("\nTesting draft_email request:")
    request = {
        'service': 'email',
        'method': 'draft_email',
        'params': {
            'to': 'team@company.com',
            'subject': 'Weekly Update',
            'body': 'Here is this week\'s status update...'
        }
    }
    result = server.process_request(request)
    print(json.dumps(result, indent=2))

    print("\n[OK] Email MCP Server tests complete")


def test_vault_mcp():
    """Test Vault MCP Server"""
    print("\n" + "="*60)
    print("Testing Vault MCP Server")
    print("="*60)

    server = MCPVaultServer(vault_path=".")

    # Show capabilities
    print("\nVault MCP Capabilities:")
    caps = server.get_capabilities()
    print(json.dumps(caps, indent=2))

    # Test get_vault_stats
    print("\nTesting get_vault_stats:")
    request = {
        'method': 'get_vault_stats'
    }
    result = server.process_request(request)
    print(json.dumps(result, indent=2))

    # Test list_tasks
    print("\nTesting list_tasks (needs_action):")
    request = {
        'method': 'list_tasks',
        'params': {
            'folder': 'needs_action'
        }
    }
    result = server.process_request(request)
    print(json.dumps(result, indent=2))

    # Test list_tasks (done)
    print("\nTesting list_tasks (done):")
    request = {
        'method': 'list_tasks',
        'params': {
            'folder': 'done'
        }
    }
    result = server.process_request(request)
    print(json.dumps(result, indent=2))

    print("\n[OK] Vault MCP Server tests complete")


def main():
    """Run all MCP tests"""
    print("\n" + "="*60)
    print("MCP Server Integration Tests")
    print("="*60)

    try:
        test_email_mcp()
        test_vault_mcp()

        print("\n" + "="*60)
        print("[OK] All MCP Server tests completed successfully!")
        print("="*60)

    except Exception as e:
        print(f"\n[ERROR] Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
