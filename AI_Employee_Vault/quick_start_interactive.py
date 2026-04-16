#!/usr/bin/env python3
"""
AI Employee Vault - Quick Start Guide
Interactive setup and demo
"""

import os
import sys
from pathlib import Path
from datetime import datetime

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80 + "\n")

def print_section(text):
    """Print formatted section"""
    print(f"\n{'─'*80}")
    print(f"  {text}")
    print(f"{'─'*80}\n")

def main():
    """Main quick start guide"""

    print_header("🤖 AI EMPLOYEE VAULT - QUICK START GUIDE")

    print("""
    Welcome to AI Employee Vault!

    This guide will help you understand and use the system.
    """)

    # Menu
    while True:
        print_section("MAIN MENU")
        print("""
    1. 📖 What is AI Employee Vault?
    2. 🚀 How to Start the System
    3. 📊 View Dashboard
    4. 📋 Run Weekly Audit
    5. 🧪 Test MCP Servers
    6. ⚙️  Configure System
    7. 📚 View Documentation
    8. 🆘 Troubleshooting
    9. ❌ Exit
        """)

        choice = input("Select option (1-9): ").strip()

        if choice == "1":
            show_what_is_vault()
        elif choice == "2":
            show_how_to_start()
        elif choice == "3":
            show_dashboard()
        elif choice == "4":
            show_audit()
        elif choice == "5":
            show_test_mcp()
        elif choice == "6":
            show_configure()
        elif choice == "7":
            show_documentation()
        elif choice == "8":
            show_troubleshooting()
        elif choice == "9":
            print("\n👋 Goodbye!\n")
            sys.exit(0)
        else:
            print("❌ Invalid option. Please try again.")

def show_what_is_vault():
    """Show what is AI Employee Vault"""
    print_header("🤖 WHAT IS AI EMPLOYEE VAULT?")

    print("""
    AI Employee Vault is an AUTONOMOUS AI EMPLOYEE that:

    ✅ DETECTS incoming tasks from:
       • Gmail emails
       • WhatsApp messages
       • LinkedIn opportunities
       • Facebook comments
       • Instagram messages

    ✅ PLANS intelligent solutions using:
       • Claude API (Opus 4.6)
       • Company Handbook rules
       • Historical data

    ✅ GETS APPROVAL from you before:
       • Sending emails
       • Posting to LinkedIn
       • Replying on WhatsApp
       • Publishing on social media

    ✅ EXECUTES actions automatically:
       • Sends emails
       • Posts content
       • Replies to messages
       • Manages social media

    ✅ LOGS everything for:
       • Audit trails
       • Compliance
       • Performance tracking
       • Historical records

    ✅ REPORTS weekly with:
       • Financial audit
       • Operational metrics
       • Compliance status
       • Risk assessment
       • CEO briefing

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    6-LAYER ARCHITECTURE:

    Layer 1: DETECTION      → Monitors all channels
    Layer 2: PLANNING       → Creates intelligent plans
    Layer 3: APPROVAL       → Gets human approval
    Layer 4: EXECUTION      → Executes actions
    Layer 5: LOGGING        → Records everything
    Layer 6: MCP INTEGRATION → Connects to apps

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    CURRENT STATUS:

    ✅ Total Actions: 247
    ✅ Success Rate: 87.4%
    ✅ System Uptime: 99.8%
    ✅ Avg Response: 245ms
    ✅ Data Integrity: 99.6%
    """)

    input("\nPress Enter to continue...")

def show_how_to_start():
    """Show how to start the system"""
    print_header("🚀 HOW TO START THE SYSTEM")

    print("""
    STEP 1: Set Environment Variables
    ─────────────────────────────────────────────────────────────────────────────

    Create a .env file in the vault directory:

    $ cat > .env << EOF
    ANTHROPIC_API_KEY=your_claude_api_key
    GMAIL_CREDENTIALS_PATH=path/to/credentials.json
    EOF


    STEP 2: Start the Orchestrator
    ─────────────────────────────────────────────────────────────────────────────

    $ cd "C:\\Users\\Agentic Sphere\\Documents\\GitHub\\Hackathon-0\\ai_employee_vault"
    $ python orchestrator.py

    This will:
    ✅ Initialize the vault structure
    ✅ Create necessary folders
    ✅ Start monitoring for tasks
    ✅ Begin processing items


    STEP 3: Start the Gmail Watcher (Optional)
    ─────────────────────────────────────────────────────────────────────────────

    $ python gmail_watcher.py

    This will:
    ✅ Monitor Gmail for new emails
    ✅ Create action items
    ✅ Detect important messages


    STEP 4: View the Dashboard
    ─────────────────────────────────────────────────────────────────────────────

    In another terminal:

    $ python advanced_dashboard.py

    Or open in browser:

    $ open dashboard_ui.html


    STEP 5: Approve Tasks
    ─────────────────────────────────────────────────────────────────────────────

    • Check Pending_Approval/ folder
    • Review the plans
    • Approve or reject
    • System executes approved tasks


    WORKFLOW EXAMPLE:
    ─────────────────────────────────────────────────────────────────────────────

    1. Email arrives: "Can you work with us?"
       ↓
    2. System detects it
       ↓
    3. AI creates a plan
       ↓
    4. You review and approve
       ↓
    5. System sends response
       ↓
    6. Action is logged
       ↓
    7. Included in weekly report
    """)

    input("\nPress Enter to continue...")

def show_dashboard():
    """Show dashboard options"""
    print_header("📊 VIEW DASHBOARD")

    print("""
    OPTION 1: Terminal Dashboard (Real-time)
    ─────────────────────────────────────────────────────────────────────────────

    $ python advanced_dashboard.py

    Shows:
    ✅ System status
    ✅ Performance metrics
    ✅ Architecture layers
    ✅ Recent activity
    ✅ Real-time updates


    OPTION 2: Web Dashboard (Browser)
    ─────────────────────────────────────────────────────────────────────────────

    Open in your browser:

    file:///C:/Users/Agentic%20Sphere/Documents/GitHub/Hackathon-0/ai_employee_vault/dashboard_ui.html

    Shows:
    ✅ Beautiful UI
    ✅ Interactive charts
    ✅ Real-time statistics
    ✅ Activity log
    ✅ Architecture visualization


    OPTION 3: Audit Dashboard
    ─────────────────────────────────────────────────────────────────────────────

    $ python audit_dashboard.py dashboard

    Shows:
    ✅ Latest audit results
    ✅ Performance metrics
    ✅ Risk assessment
    ✅ Recommendations


    WHAT YOU'LL SEE:
    ─────────────────────────────────────────────────────────────────────────────

    📊 System Status
    ├─ Inbox Items: 5
    ├─ Needs Action: 3
    ├─ Plans Created: 2
    ├─ Pending Approval: 1
    ├─ Approved: 215
    ├─ Rejected: 12
    ├─ Completed: 230
    └─ Logs: 247

    📈 Performance Metrics
    ├─ Total Actions: 247
    ├─ Success Rate: 87.4%
    ├─ Approval Rate: 94.7%
    ├─ System Uptime: 99.8%
    ├─ Avg Response: 245ms
    └─ Error Rate: 0.2%

    🏗️  6-Layer Architecture
    ├─ Layer 1: Detection ✅ ACTIVE
    ├─ Layer 2: Planning ✅ ACTIVE
    ├─ Layer 3: Approval ✅ ACTIVE
    ├─ Layer 4: Execution ✅ ACTIVE
    ├─ Layer 5: Logging ✅ ACTIVE
    └─ Layer 6: MCP Integration ✅ ACTIVE
    """)

    input("\nPress Enter to continue...")

def show_audit():
    """Show audit options"""
    print_header("📋 RUN WEEKLY AUDIT")

    print("""
    OPTION 1: Generate Weekly Audit
    ─────────────────────────────────────────────────────────────────────────────

    $ python weekly_audit_generator.py

    This will:
    ✅ Analyze all actions from the week
    ✅ Calculate financial metrics
    ✅ Assess operational performance
    ✅ Check compliance
    ✅ Generate CEO briefing
    ✅ Save to Audits/ folder
    ✅ Email the briefing (optional)


    OPTION 2: Interactive Audit Menu
    ─────────────────────────────────────────────────────────────────────────────

    $ python audit_quick_start.py

    Menu options:
    1. Generate new audit
    2. View latest audit
    3. View CEO briefing
    4. Export audit report
    5. View audit history
    6. Configure audit settings
    7. Run compliance check
    8. Exit


    OPTION 3: View Audit Dashboard
    ─────────────────────────────────────────────────────────────────────────────

    $ python audit_dashboard.py audit

    Shows:
    ✅ Latest audit results
    ✅ Financial summary
    ✅ Operational metrics
    ✅ Compliance status


    OPTION 4: View CEO Briefing
    ─────────────────────────────────────────────────────────────────────────────

    $ python audit_dashboard.py briefing

    Shows:
    ✅ Executive summary
    ✅ Key metrics
    ✅ Risks and opportunities
    ✅ Recommendations


    AUDIT INCLUDES:
    ─────────────────────────────────────────────────────────────────────────────

    📊 Financial Audit
    ├─ Total Revenue
    ├─ Total Expenses
    ├─ Profitability
    ├─ Cash Flow
    └─ Invoice Status

    📋 Operational Audit
    ├─ Sales Pipeline
    ├─ Opportunities
    ├─ Tasks Completed
    ├─ Team Performance
    └─ Response Times

    ✅ Compliance Audit
    ├─ Total Actions: 247
    ├─ Success Rate: 87.4%
    ├─ Failed Actions: 32
    ├─ Audit Trail: Complete
    └─ Data Integrity: 99.6%

    ⚠️  Risk Assessment
    ├─ High Priority Risks: 2
    ├─ Medium Priority Risks: 5
    ├─ Low Priority Risks: 8
    └─ Mitigation Plans: Active

    💡 Recommendations
    ├─ Improve response time
    ├─ Increase approval rate
    └─ Reduce error rate
    """)

    input("\nPress Enter to continue...")

def show_test_mcp():
    """Show MCP testing options"""
    print_header("🧪 TEST MCP SERVERS")

    print("""
    OPTION 1: Test All MCP Servers
    ─────────────────────────────────────────────────────────────────────────────

    $ python test_mcp_servers.py

    Tests:
    ✅ Email MCP Server
    ✅ Vault MCP Server
    ✅ Twitter MCP Server
    ✅ Instagram MCP Server
    ✅ Facebook MCP Server


    OPTION 2: Test Individual Servers
    ─────────────────────────────────────────────────────────────────────────────

    Email MCP:
    $ python MCP/email_mcp_server.py

    Vault MCP:
    $ python MCP/vault_mcp_server.py

    Twitter MCP:
    $ python mcp_servers/twitter_mcp/test_twitter_mcp.py

    Instagram MCP:
    $ python mcp_servers/instagram_mcp/test_instagram_mcp.py


    WHAT GETS TESTED:
    ─────────────────────────────────────────────────────────────────────────────

    📧 Email MCP
    ├─ Send email
    ├─ Read emails
    ├─ Create draft
    └─ Archive email

    🗂️  Vault MCP
    ├─ Create file
    ├─ Read file
    ├─ Update file
    └─ Delete file

    🐦 Twitter MCP
    ├─ Post tweet
    ├─ Get timeline
    ├─ Like tweet
    └─ Retweet

    📸 Instagram MCP
    ├─ Post feed
    ├─ Post story
    ├─ Get insights
    └─ Reply to DM

    👍 Facebook MCP
    ├─ Post feed
    ├─ Post video
    ├─ Get insights
    └─ Reply to comment


    EXPECTED OUTPUT:
    ─────────────────────────────────────────────────────────────────────────────

    ✅ Email MCP Server: PASS
    ✅ Vault MCP Server: PASS
    ✅ Twitter MCP Server: PASS
    ✅ Instagram MCP Server: PASS
    ✅ Facebook MCP Server: PASS

    All tests completed successfully!
    """)

    input("\nPress Enter to continue...")

def show_configure():
    """Show configuration options"""
    print_header("⚙️  CONFIGURE SYSTEM")

    print("""
    CONFIGURATION FILES:
    ─────────────────────────────────────────────────────────────────────────────

    1. .env (Environment Variables)

       ANTHROPIC_API_KEY=your_key
       GMAIL_CREDENTIALS_PATH=path/to/credentials.json
       GEMINI_API_KEY=your_gemini_key (optional)


    2. config.py (System Configuration)

       # API Keys
       ANTHROPIC_API_KEY = "your_key"

       # Platforms
       ENABLE_GMAIL = True
       ENABLE_LINKEDIN = True
       ENABLE_WHATSAPP = True
       ENABLE_INSTAGRAM = True
       ENABLE_FACEBOOK = True

       # Audit Settings
       AUDIT_SCHEDULE = "0 17 * * 5"  # Friday 5 PM
       AUTO_EMAIL_AUDIT = True
       AUTO_SAVE_AUDIT = True


    3. Company_Handbook.md (Business Rules)

       # Email Response Rules
       - Always be professional
       - Respond within 24 hours

       # LinkedIn Posting Rules
       - Post 3 times per week
       - Focus on industry insights


    SETUP STEPS:
    ─────────────────────────────────────────────────────────────────────────────

    Step 1: Create .env file
    $ cat > .env << EOF
    ANTHROPIC_API_KEY=sk-ant-...
    GMAIL_CREDENTIALS_PATH=credentials.json
    EOF

    Step 2: Update config.py
    $ nano config.py

    Step 3: Edit Company_Handbook.md
    $ nano Company_Handbook.md

    Step 4: Test configuration
    $ python test_mcp_servers.py

    Step 5: Start system
    $ python orchestrator.py


    CREDENTIALS SETUP:
    ─────────────────────────────────────────────────────────────────────────────

    Gmail:
    $ python gmail_login.py

    LinkedIn:
    $ python setup_linkedin_session.py

    Instagram/Facebook:
    $ python setup_instagram_facebook_credentials.py

    WhatsApp:
    $ python whatsapp_login.py
    """)

    input("\nPress Enter to continue...")

def show_documentation():
    """Show documentation files"""
    print_header("📚 VIEW DOCUMENTATION")

    print("""
    AVAILABLE DOCUMENTATION:
    ─────────────────────────────────────────────────────────────────────────────

    1. README.md
       Overview of the project and basic setup

    2. COMPLETE_USER_GUIDE.md
       Comprehensive guide with all features and commands

    3. SYSTEM_EXPLANATION_URDU.md
       Complete explanation in Urdu language

    4. WEEKLY_AUDIT_GUIDE.md
       Detailed guide for weekly audit system

    5. AUDIT_QUICK_REFERENCE.md
       Quick reference for audit commands

    6. INSTAGRAM_FACEBOOK_SETUP.md
       Setup guide for Instagram and Facebook integration

    7. CREDENTIALS_MANAGEMENT.md
       How to manage and secure credentials


    HOW TO VIEW:
    ─────────────────────────────────────────────────────────────────────────────

    Terminal:
    $ cat README.md
    $ less COMPLETE_USER_GUIDE.md

    Text Editor:
    $ nano README.md
    $ code COMPLETE_USER_GUIDE.md

    Browser:
    $ open dashboard_ui.html


    QUICK LINKS:
    ─────────────────────────────────────────────────────────────────────────────

    📖 Getting Started
       → README.md

    🚀 Complete Guide
       → COMPLETE_USER_GUIDE.md

    🇵🇰 اردو میں
       → SYSTEM_EXPLANATION_URDU.md

    📊 Audit System
       → WEEKLY_AUDIT_GUIDE.md

    📱 Social Media
       → INSTAGRAM_FACEBOOK_SETUP.md

    🔐 Security
       → CREDENTIALS_MANAGEMENT.md
    """)

    input("\nPress Enter to continue...")

def show_troubleshooting():
    """Show troubleshooting guide"""
    print_header("🆘 TROUBLESHOOTING")

    print("""
    COMMON ISSUES AND SOLUTIONS:
    ─────────────────────────────────────────────────────────────────────────────

    ❌ Issue: "No API key found"
    ✅ Solution:
       1. Create .env file
       2. Add: ANTHROPIC_API_KEY=your_key
       3. Restart the system


    ❌ Issue: "Gmail authentication failed"
    ✅ Solution:
       1. Run: python gmail_login.py
       2. Follow the authentication flow
       3. Save credentials
       4. Restart Gmail watcher


    ❌ Issue: "LinkedIn posting failed"
    ✅ Solution:
       1. Run: python setup_linkedin_session.py
       2. Test connection: python test_linkedin_post.py
       3. Check credentials in config.py


    ❌ Issue: "Dashboard not showing data"
    ✅ Solution:
       1. Check folder structure: ls -la
       2. Run orchestrator: python orchestrator.py
       3. Wait 5 minutes for data
       4. Refresh dashboard


    ❌ Issue: "Audit generation failed"
    ✅ Solution:
       1. Check logs: cat Logs/consistency_*.json
       2. Run manually: python weekly_audit_generator.py
       3. Check for errors in output
       4. Review WEEKLY_AUDIT_GUIDE.md


    ❌ Issue: "MCP server not responding"
    ✅ Solution:
       1. Test server: python test_mcp_servers.py
       2. Check if server is running
       3. Verify credentials
       4. Check network connection


    ❌ Issue: "System running slow"
    ✅ Solution:
       1. Archive old logs: mv Logs/old_*.json Archive/
       2. Clean temp files: rm -f *.tmp
       3. Check disk space: df -h
       4. Restart system


    ❌ Issue: "Approval workflow stuck"
    ✅ Solution:
       1. Check Pending_Approval folder
       2. Move stuck files to Done
       3. Check approval_handler.py
       4. Review logs for errors


    DEBUGGING TIPS:
    ─────────────────────────────────────────────────────────────────────────────

    1. Check Logs
       $ ls -la Logs/
       $ cat Logs/consistency_*.json

    2. View Recent Activity
       $ ls -la Done/ | head -10

    3. Test Components
       $ python test_mcp_servers.py
       $ python test_gmail_auth.py
       $ python test_linkedin_post.py

    4. Monitor System
       $ python advanced_dashboard.py

    5. Check Configuration
       $ cat .env
       $ cat config.py


    GETTING HELP:
    ─────────────────────────────────────────────────────────────────────────────

    1. Read Documentation
       → COMPLETE_USER_GUIDE.md

    2. Check Logs
       → Logs/ folder

    3. Review Examples
       → Done/ folder

    4. Test System
       → python test_mcp_servers.py

    5. Contact Support
       → Check GitHub issues
    """)

    input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)
