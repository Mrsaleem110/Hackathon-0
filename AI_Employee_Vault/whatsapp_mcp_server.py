"""
WhatsApp MCP Server for AI Employee Vault
Provides manual WhatsApp message handling through MCP protocol
"""

import json
import sys
from pathlib import Path
from datetime import datetime


class WhatsAppMCPServer:
    """MCP Server for WhatsApp operations"""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.needs_action = vault_path / "Needs_Action"
        self.needs_action.mkdir(exist_ok=True)

    def handle_request(self, request: dict) -> dict:
        """Handle MCP request"""
        method = request.get("method")

        if method == "tools/list":
            return self.list_tools()
        elif method == "tools/call":
            return self.call_tool(request.get("params", {}))
        else:
            return {"error": f"Unknown method: {method}"}

    def list_tools(self) -> dict:
        """List available WhatsApp tools"""
        return {
            "tools": [
                {
                    "name": "create_whatsapp_task",
                    "description": "Create a task from a WhatsApp message",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "sender": {"type": "string", "description": "Message sender name"},
                            "message": {"type": "string", "description": "Message content"},
                            "priority": {"type": "string", "enum": ["low", "medium", "high"], "default": "medium"}
                        },
                        "required": ["sender", "message"]
                    }
                },
                {
                    "name": "list_whatsapp_tasks",
                    "description": "List all WhatsApp tasks in vault",
                    "inputSchema": {"type": "object", "properties": {}}
                },
                {
                    "name": "send_whatsapp_reply",
                    "description": "Draft a WhatsApp reply (manual sending required)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "recipient": {"type": "string", "description": "Recipient name"},
                            "message": {"type": "string", "description": "Reply message"}
                        },
                        "required": ["recipient", "message"]
                    }
                }
            ]
        }

    def call_tool(self, params: dict) -> dict:
        """Execute tool call"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        if tool_name == "create_whatsapp_task":
            return self.create_task(arguments)
        elif tool_name == "list_whatsapp_tasks":
            return self.list_tasks()
        elif tool_name == "send_whatsapp_reply":
            return self.draft_reply(arguments)
        else:
            return {"error": f"Unknown tool: {tool_name}"}

    def create_task(self, args: dict) -> dict:
        """Create WhatsApp task file"""
        sender = args.get("sender", "Unknown")
        message = args.get("message", "")
        priority = args.get("priority", "medium")

        # Create filename
        sender_slug = sender.lower().replace(" ", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"WHATSAPP_{sender_slug}_{timestamp}.md"
        filepath = self.needs_action / filename

        # Create content
        content = f"""---
type: whatsapp
from: "{sender}"
received: "{datetime.now().isoformat()}"
priority: {priority}
status: pending
source: whatsapp_mcp
---

## Message from {sender}
{message}

## Suggested Actions
- [ ] Read and understand the message
- [ ] Determine appropriate response
- [ ] Draft reply
- [ ] Send reply manually via WhatsApp
- [ ] Mark as complete

## Metadata
- Created: {datetime.now().isoformat()}
- Priority: {priority}
- Source: WhatsApp MCP Server
"""

        filepath.write_text(content, encoding='utf-8')

        return {
            "content": [
                {
                    "type": "text",
                    "text": f"✅ WhatsApp task created: {filename}\nPriority: {priority}\nFrom: {sender}"
                }
            ]
        }

    def list_tasks(self) -> dict:
        """List all WhatsApp tasks"""
        whatsapp_files = list(self.needs_action.glob("WHATSAPP_*.md"))

        if not whatsapp_files:
            return {
                "content": [
                    {"type": "text", "text": "No WhatsApp tasks found in Needs_Action"}
                ]
            }

        tasks = []
        for file in whatsapp_files:
            content = file.read_text(encoding='utf-8')
            tasks.append(f"- {file.name}")

        result = f"Found {len(tasks)} WhatsApp tasks:\n" + "\n".join(tasks)

        return {
            "content": [
                {"type": "text", "text": result}
            ]
        }

    def draft_reply(self, args: dict) -> dict:
        """Draft a WhatsApp reply"""
        recipient = args.get("recipient", "Unknown")
        message = args.get("message", "")

        # Create draft file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"WHATSAPP_REPLY_{recipient.lower().replace(' ', '_')}_{timestamp}.md"
        filepath = self.vault_path / "Pending_Approval" / filename

        content = f"""---
type: whatsapp_reply
to: "{recipient}"
created: "{datetime.now().isoformat()}"
status: draft
---

## WhatsApp Reply Draft

**To:** {recipient}

**Message:**
{message}

## Instructions
1. Review the message above
2. Copy the message
3. Open WhatsApp and find {recipient}
4. Paste and send the message
5. Move this file to Done/ when sent

---
*Draft created by WhatsApp MCP Server*
"""

        filepath.write_text(content, encoding='utf-8')

        return {
            "content": [
                {
                    "type": "text",
                    "text": f"✅ Reply draft created: {filename}\n\nTo: {recipient}\n\nMessage saved to Pending_Approval/\nPlease send manually via WhatsApp."
                }
            ]
        }


def main():
    """Main MCP server loop"""
    vault_path = Path(".")
    server = WhatsAppMCPServer(vault_path)

    print("WhatsApp MCP Server started", file=sys.stderr)

    for line in sys.stdin:
        try:
            request = json.loads(line)
            response = server.handle_request(request)
            print(json.dumps(response))
            sys.stdout.flush()
        except Exception as e:
            error_response = {"error": str(e)}
            print(json.dumps(error_response))
            sys.stdout.flush()


if __name__ == "__main__":
    main()
