"""
Reasoning Engine for AI Employee Vault
Creates Plan.md files for multi-step tasks using Claude API or Google Gemini
Implements intelligent task planning with multiple AI providers
"""

import time
import logging
from pathlib import Path
from datetime import datetime
import json
import subprocess
import sys
import os

# Import AI providers
try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class ReasoningEngine:
    """Orchestrates AI providers (Claude API or Google Gemini) for intelligent task planning"""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.plans = self.vault_path / 'Plans'
        self.done = self.vault_path / 'Done'
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.logs = self.vault_path / 'Logs'

        # Create directories
        self.plans.mkdir(exist_ok=True)
        self.done.mkdir(exist_ok=True)
        self.logs.mkdir(exist_ok=True)

        # Set up logging
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Initialize AI provider
        self.provider = None
        self.client = None
        self.model = None

        # Check for Gemini API first (user preference)
        gemini_key = os.getenv('GEMINI_API_KEY')
        if gemini_key and GEMINI_AVAILABLE:
            genai.configure(api_key=gemini_key)
            self.provider = 'gemini'
            self.model = 'gemini-2.5-flash'
            self.logger.info("✓ Google Gemini API client initialized successfully")
        # Fall back to Claude API
        elif ANTHROPIC_AVAILABLE:
            claude_key = os.getenv('ANTHROPIC_API_KEY')
            if claude_key:
                self.client = Anthropic(api_key=claude_key)
                self.provider = 'claude'
                self.model = 'claude-opus-4-6'
                self.logger.info("✓ Claude API client initialized successfully")
            else:
                self.logger.warning("No API keys found. Using fallback plan generation.")
        else:
            self.logger.warning("No AI providers available. Using fallback plan generation.")

    def get_pending_tasks(self) -> list:
        """Get all pending tasks from Needs_Action folder"""
        tasks = []
        for file in self.needs_action.glob('*.md'):
            try:
                content = file.read_text(encoding='utf-8')
                tasks.append({
                    'file': file,
                    'filename': file.name,
                    'content': content
                })
            except Exception as e:
                self.logger.error(f"Error reading task file: {e}")

        return tasks

    def create_plan_prompt(self, task: dict) -> str:
        """Create a prompt for Claude to analyze task and create plan"""
        prompt = f"""You are an AI Employee analyzing a task from the Needs_Action folder.

TASK FILE: {task['filename']}

TASK CONTENT:
{task['content']}

INSTRUCTIONS:
1. Analyze this task carefully
2. Break it down into clear, actionable steps
3. Identify what requires human approval
4. Estimate time and resources needed
5. Assess any risks or dependencies

RESPOND WITH A PLAN IN THIS FORMAT:

## Objective
[Clear statement of what needs to be accomplished]

## Analysis
[Your analysis of the task, including priority and complexity]

## Steps
- [ ] Step 1: [Description]
- [ ] Step 2: [Description]
- [ ] Step 3: [Description]

## Approval Required
[List any steps that need human approval - be specific about what needs approval]

## Estimated Time
[Your time estimate in minutes]

## Risk Assessment
[Any risks or dependencies to consider]

## Next Action
[What should happen next]
"""
        return prompt

    def generate_plan_with_ai(self, task: dict) -> str:
        """Call AI provider (Gemini or Claude) to generate an intelligent plan"""
        if not self.provider:
            self.logger.warning("No AI provider available, using fallback plan generation")
            return self._generate_fallback_plan(task)

        prompt = self.create_plan_prompt(task)

        try:
            if self.provider == 'gemini':
                return self._generate_plan_with_gemini(prompt, task)
            elif self.provider == 'claude':
                return self._generate_plan_with_claude(prompt, task)
        except Exception as e:
            self.logger.error(f"Error calling AI provider: {e}")
            return self._generate_fallback_plan(task)

    def _generate_plan_with_gemini(self, prompt: str, task: dict) -> str:
        """Generate plan using Google Gemini API"""
        try:
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(prompt)
            plan_content = response.text
            self.logger.info(f"Plan generated by Gemini for: {task['filename']}")
            return plan_content
        except Exception as e:
            self.logger.error(f"Error calling Gemini API: {e}")
            return self._generate_fallback_plan(task)

    def _generate_plan_with_claude(self, prompt: str, task: dict) -> str:
        """Generate plan using Claude API"""
        try:
            message = self.client.messages.create(
                model="claude-opus-4-6",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            plan_content = message.content[0].text
            self.logger.info(f"Plan generated by Claude for: {task['filename']}")
            return plan_content
        except Exception as e:
            self.logger.error(f"Error calling Claude API: {e}")
            return self._generate_fallback_plan(task)

    def _generate_fallback_plan(self, task: dict) -> str:
        """Generate a basic plan when Claude API is unavailable"""
        return f"""## Objective
Process task: {task['filename']}

## Analysis
This task requires processing and execution.

## Steps
- [ ] Review task details
- [ ] Determine required actions
- [ ] Execute or escalate
- [ ] Update status

## Approval Required
Review and approval by human operator

## Estimated Time
30 minutes

## Next Action
Move to Pending_Approval for human review
"""

    def create_plan_file(self, task: dict, plan_content: str) -> Path:
        """Create a Plan.md file from Claude's analysis"""
        # Extract task name from filename
        task_name = task['filename'].replace('.md', '')

        plan_file = self.plans / f"PLAN_{task_name}.md"

        content = f"""---
created: {datetime.now().isoformat()}
status: pending_execution
source_task: {task['filename']}
---

# Task Plan: {task_name}

{plan_content}

## Status Tracking
- [ ] Plan reviewed
- [ ] Approved for execution
- [ ] Execution started
- [ ] Execution completed
- [ ] Results verified

## Approval Workflow
To approve this plan:
1. Review the steps above
2. Move this file to /Pending_Approval/Approved/
3. AI Employee will execute the plan

To reject:
1. Move this file to /Pending_Approval/Rejected/
2. Add rejection reason in comments

---
*Generated by Claude Reasoning Engine*
*{datetime.now().isoformat()}*
"""

        try:
            plan_file.write_text(content, encoding='utf-8')
            self.logger.info(f"Created plan file: {plan_file}")
        except Exception as e:
            self.logger.error(f"Error creating plan file: {e}")

        return plan_file

    def log_reasoning_action(self, action: str, task_name: str, status: str):
        """Log reasoning action to audit trail"""
        log_file = self.logs / f"{datetime.now().strftime('%Y-%m-%d')}.json"

        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'task': task_name,
            'status': status,
            'component': 'reasoning_engine'
        }

        try:
            if log_file.exists():
                logs = json.loads(log_file.read_text())
            else:
                logs = []

            logs.append(log_entry)
            log_file.write_text(json.dumps(logs, indent=2), encoding='utf-8')
        except Exception as e:
            self.logger.error(f"Error logging action: {e}")

    def process_tasks(self):
        """Process all pending tasks and create plans using AI provider"""
        tasks = self.get_pending_tasks()

        if not tasks:
            self.logger.info("No pending tasks to process")
            return

        self.logger.info(f"Found {len(tasks)} pending tasks")

        for task in tasks:
            try:
                self.logger.info(f"Processing task: {task['filename']}")

                # Generate plan with AI provider
                plan_content = self.generate_plan_with_ai(task)

                if plan_content:
                    # Create plan file
                    plan_file = self.create_plan_file(task, plan_content)

                    # Log action
                    self.log_reasoning_action(
                        'plan_created',
                        task['filename'],
                        'success'
                    )

                    self.logger.info(f"Plan created: {plan_file}")
                else:
                    self.logger.error(f"Failed to generate plan for: {task['filename']}")
                    self.log_reasoning_action(
                        'plan_creation_failed',
                        task['filename'],
                        'failed'
                    )

            except Exception as e:
                self.logger.error(f"Error processing task {task['filename']}: {e}")
                self.log_reasoning_action(
                    'plan_creation_failed',
                    task['filename'],
                    'failed'
                )

    def demo_run(self):
        """Demo run that creates sample plans using Claude API"""
        self.logger.info("Running Claude Reasoning Engine in demo mode")

        # Create sample task files
        sample_tasks = [
            {
                'filename': 'WHATSAPP_client_a_urgent.md',
                'content': """---
type: whatsapp
from: "Client A"
priority: high
---

## Message Preview
urgent: can you send the invoice asap?

## Sender
Client A"""
            },
            {
                'filename': 'GMAIL_invoice_payment.md',
                'content': """---
type: email
from: "accounts@client1.com"
subject: "Invoice Payment Required"
priority: high
---

## Email Content
Your invoice #1234 is overdue. Please process payment asap."""
            }
        ]

        for task in sample_tasks:
            try:
                # Generate plan using Claude API
                plan_content = self.generate_plan_with_claude(task)

                if plan_content:
                    # Create plan file
                    self.create_plan_file(task, plan_content)
                    self.logger.info(f"Created demo plan for: {task['filename']}")
                else:
                    self.logger.error(f"Failed to create plan for: {task['filename']}")

            except Exception as e:
                self.logger.error(f"Error in demo run for {task['filename']}: {e}")

        self.logger.info(f"Demo run completed")


if __name__ == "__main__":
    # Initialize the reasoning engine
    VAULT_PATH = Path(".")

    engine = ReasoningEngine(vault_path=VAULT_PATH)

    # Check which AI provider is available
    if engine.provider:
        print(f"\n✓ {engine.provider.upper()} API client initialized")
        print(f"Processing pending tasks with {engine.provider.upper()} API...\n")
        engine.process_tasks()
    else:
        print("\n✗ No AI provider available")
        print("Set GEMINI_API_KEY or ANTHROPIC_API_KEY environment variable")
        print("\nRunning in fallback mode...\n")
        engine.process_tasks()

    print(f"\nReasoning Engine setup complete!")
    print(f"Plans created in: {engine.plans}")
    print(f"AI Provider: {engine.provider if engine.provider else 'Fallback Mode'}")
    print(f"\nTo process pending tasks:")
    print(f"  engine.process_tasks()")
