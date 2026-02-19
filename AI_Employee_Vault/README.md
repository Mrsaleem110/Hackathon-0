# Bronze Tier: Personal AI Employee - Foundation

## Overview
This project implements the Bronze Tier requirements for the Personal AI Employee Hackathon. The goal is to create a foundation for an autonomous AI employee that manages personal and business affairs.

## Architecture Components Implemented

### 1. Obsidian Vault Structure
- **Dashboard.md** - Real-time summary of personal/business affairs
- **Company_Handbook.md** - Rules of engagement and protocols
- **Folder Structure**:
  - `/Inbox` - For incoming items to be processed
  - `/Needs_Action` - Items requiring AI processing
  - `/Done` - Completed tasks

### 2. Watcher System
- **Gmail Watcher** - Monitors Gmail for important messages
- Creates action files in the `Needs_Action` folder
- Implements priority detection for urgent messages

### 3. Processing System
- **Orchestrator** - Processes items in `Needs_Action` folder
- Moves completed items to `Done` folder
- Updates Dashboard with processing activity

### 4. Agent Skills
- **Email Processor** - Skill for processing email requests
- Demonstrates the agent skill functionality required by the hackathon

## How It Works

### 1. Monitoring
- The Gmail Watcher continuously monitors for new emails
- When important emails are detected, they are converted to markdown files in `/Needs_Action/`

### 2. Processing
- The Orchestrator checks the `/Needs_Action/` folder for new items
- Each item is processed according to the Company Handbook rules
- Files are moved to `/Done/` when completed

### 3. Reporting
- The Dashboard is updated with recent activity
- All actions are logged for review

## Files Created

- `Dashboard.md` - Real-time status dashboard
- `Company_Handbook.md` - Rules and guidelines for AI behavior
- `gmail_watcher.py` - Monitors Gmail for new messages
- `orchestrator.py` - Processes items in the workflow
- `Skills/email_processor.py` - Agent skill for email processing
- `/Inbox/` - Folder for incoming items
- `/Needs_Action/` - Folder for items needing processing (with sample files)
- `/Done/` - Folder for completed items

## Setup Instructions

1. Ensure Claude Code is installed and configured
2. Install required Python packages:
   ```bash
   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```
3. Place all files in your AI Employee Vault directory
4. Run the Gmail Watcher to create sample action files:
   ```bash
   python gmail_watcher.py
   ```
5. Run the Orchestrator to process action files:
   ```bash
   python orchestrator.py
   ```

## Security Notes

- Credentials are handled securely (in demo mode, credentials are not required)
- All data stays local in the Obsidian vault
- Human-in-the-loop approval for sensitive actions
- Audit logging of all AI actions

## Next Steps (Silver/Gold Tier)

- Add more watcher types (WhatsApp, file system, etc.)
- Implement MCP servers for external actions
- Add more sophisticated processing rules
- Create automated scheduling
- Implement the "Monday Morning CEO Briefing" feature

## Demo Flow

The system demonstrates the complete flow:
1. Gmail Watcher creates sample action files
2. Orchestrator processes these files
3. Dashboard is updated with activity
4. Files are moved from Needs_Action to Done

This creates a foundation for building a more sophisticated autonomous AI employee system.