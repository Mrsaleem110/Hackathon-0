"""
Process Real WhatsApp Task - Client A Invoice
"""
import sys
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from whatsapp_mcp_server import WhatsAppMCPServer

# Initialize server
vault_path = Path(".")
server = WhatsAppMCPServer(vault_path)

print("="*60)
print("Processing Real WhatsApp Message")
print("="*60)

# Create task from real message
result = server.create_task({
    "sender": "Client A",
    "message": "urgent: can you send the invoice asap? we need it for our records. Invoice #1234 for $5,000",
    "priority": "high"
})

print("\n✅ Task Created:")
print(result["content"][0]["text"])

# Draft reply
print("\n" + "="*60)
print("Drafting Reply")
print("="*60)

reply_result = server.draft_reply({
    "recipient": "Client A",
    "message": """Hi! I'll send Invoice #1234 ($5,000) right away via email to agentic_sphere@gmail.com.

You should receive it within the next few minutes.

Thanks for your patience!"""
})

print("\n✅ Reply Drafted:")
print(reply_result["content"][0]["text"])

# List all tasks
print("\n" + "="*60)
print("All WhatsApp Tasks")
print("="*60)

tasks_result = server.list_tasks()
print("\n" + tasks_result["content"][0]["text"])

print("\n" + "="*60)
print("Next Steps:")
print("="*60)
print("1. Check Pending_Approval/ for reply draft")
print("2. Review and copy the message")
print("3. Send via WhatsApp to Client A")
print("4. Move task to Done/ when complete")
print("="*60)
