"""Enhanced Orchestrator - Ralph Wiggum Loop with step verification"""

import os
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Task:
    """Task with steps"""

    def __init__(self, task_id: str, title: str, steps: List[Dict[str, Any]]):
        """Initialize task"""
        self.task_id = task_id
        self.title = title
        self.steps = steps
        self.status = 'pending'
        self.created_at = datetime.now().isoformat()
        self.completed_at = None
        self.step_results = []

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'task_id': self.task_id,
            'title': self.title,
            'status': self.status,
            'steps': self.steps,
            'created_at': self.created_at,
            'completed_at': self.completed_at,
            'step_results': self.step_results
        }


class EnhancedOrchestrator:
    """Enhanced orchestrator with step verification"""

    def __init__(self, vault_path: str = '.'):
        """Initialize enhanced orchestrator"""
        self.vault_path = Path(vault_path)
        self.tasks_path = self.vault_path / 'Tasks'
        self.tasks_path.mkdir(exist_ok=True)
        self.execution_log = []

        logger.info(f"Enhanced Orchestrator initialized at {self.vault_path}")

    def execute_task_with_verification(self, task: Task) -> bool:
        """Execute task with step-by-step verification (Ralph Wiggum Loop)"""
        try:
            logger.info(f"Starting task execution: {task.title}")
            task.status = 'in_progress'

            steps = task.steps
            total_steps = len(steps)

            for i, step in enumerate(steps):
                step_num = i + 1
                logger.info(f"\n{'='*60}")
                logger.info(f"Step {step_num}/{total_steps}: {step.get('name', 'Unknown')}")
                logger.info(f"{'='*60}")

                try:
                    # Execute step
                    logger.info(f"Executing step {step_num}...")
                    result = self.execute_step(step)

                    # Verify step completion
                    logger.info(f"Verifying step {step_num}...")
                    if not self.verify_step(step, result):
                        logger.error(f"❌ Step {step_num} verification failed")
                        logger.info(f"Attempting rollback for step {step_num}...")

                        # Try rollback
                        if step.get('has_rollback'):
                            self.rollback_step(step)

                        # Report failure
                        self.report_step_failure(task, step, step_num)
                        task.status = 'failed'
                        return False

                    logger.info(f"✅ Step {step_num} completed successfully")
                    task.step_results.append({
                        'step': step_num,
                        'name': step.get('name'),
                        'status': 'success',
                        'result': result
                    })

                except Exception as e:
                    logger.error(f"❌ Step {step_num} failed with exception: {e}")
                    self.report_step_failure(task, step, step_num, error=e)
                    task.status = 'failed'
                    return False

            logger.info(f"\n{'='*60}")
            logger.info(f"✅ Task {task.title} completed successfully")
            logger.info(f"{'='*60}")

            task.status = 'completed'
            task.completed_at = datetime.now().isoformat()
            self.save_task(task)

            return True

        except Exception as e:
            logger.error(f"Fatal error in task execution: {e}")
            task.status = 'failed'
            return False

    def execute_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single step"""
        try:
            step_type = step.get('type', 'unknown')
            action = step.get('action', 'unknown')

            logger.info(f"  Type: {step_type}")
            logger.info(f"  Action: {action}")

            # Simulate step execution
            result = {
                'success': True,
                'step_type': step_type,
                'action': action,
                'timestamp': datetime.now().isoformat(),
                'output': f'Step {action} executed successfully'
            }

            logger.info(f"  Result: {result['output']}")
            return result

        except Exception as e:
            logger.error(f"Error executing step: {e}")
            return {'success': False, 'error': str(e)}

    def verify_step(self, step: Dict[str, Any], result: Dict[str, Any]) -> bool:
        """Verify step completion"""
        try:
            if not result.get('success'):
                logger.warning(f"Step result indicates failure: {result.get('error')}")
                return False

            # Check expected output
            expected_output = step.get('expected_output')
            if expected_output:
                actual_output = result.get('output', '')
                if expected_output not in actual_output:
                    logger.warning(f"Expected output not found: {expected_output}")
                    return False

            logger.info(f"  ✅ Verification passed")
            return True

        except Exception as e:
            logger.error(f"Error verifying step: {e}")
            return False

    def rollback_step(self, step: Dict[str, Any]) -> bool:
        """Rollback a step"""
        try:
            rollback_action = step.get('rollback_action')
            logger.info(f"  Executing rollback: {rollback_action}")

            # Simulate rollback
            logger.info(f"  ✅ Rollback completed")
            return True

        except Exception as e:
            logger.error(f"Error rolling back step: {e}")
            return False

    def report_step_failure(self, task: Task, step: Dict[str, Any], step_num: int, error: Exception = None):
        """Report step failure"""
        try:
            failure_report = {
                'task_id': task.task_id,
                'task_title': task.title,
                'step_num': step_num,
                'step_name': step.get('name'),
                'error': str(error) if error else 'Verification failed',
                'timestamp': datetime.now().isoformat()
            }

            self.execution_log.append(failure_report)
            logger.error(f"Failure report: {failure_report}")

            # Save failure report
            report_file = self.tasks_path / f"failure_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_file, 'w') as f:
                json.dump(failure_report, f, indent=2)

        except Exception as e:
            logger.error(f"Error reporting failure: {e}")

    def save_task(self, task: Task):
        """Save task to file"""
        try:
            task_file = self.tasks_path / f"{task.task_id}.json"
            with open(task_file, 'w') as f:
                json.dump(task.to_dict(), f, indent=2)
            logger.info(f"Task saved to {task_file}")
        except Exception as e:
            logger.error(f"Error saving task: {e}")

    def get_execution_stats(self) -> Dict[str, Any]:
        """Get execution statistics"""
        try:
            total_tasks = len(list(self.tasks_path.glob("*.json")))
            total_failures = len(self.execution_log)

            return {
                'total_tasks': total_tasks,
                'total_failures': total_failures,
                'success_rate': ((total_tasks - total_failures) / total_tasks * 100) if total_tasks > 0 else 0,
                'execution_log_entries': len(self.execution_log)
            }

        except Exception as e:
            logger.error(f"Error getting execution stats: {e}")
            return {}


# Example usage
if __name__ == "__main__":
    # Create orchestrator
    orchestrator = EnhancedOrchestrator()

    # Create a sample task with steps
    sample_task = Task(
        task_id="task_001",
        title="Send Email Campaign",
        steps=[
            {
                'name': 'Validate Recipients',
                'type': 'validation',
                'action': 'validate_email_list',
                'expected_output': 'validation passed',
                'has_rollback': False
            },
            {
                'name': 'Generate Email Content',
                'type': 'generation',
                'action': 'generate_email_content',
                'expected_output': 'content generated',
                'has_rollback': False
            },
            {
                'name': 'Send Emails',
                'type': 'action',
                'action': 'send_emails',
                'expected_output': 'emails sent',
                'has_rollback': True,
                'rollback_action': 'recall_emails'
            },
            {
                'name': 'Log Results',
                'type': 'logging',
                'action': 'log_campaign_results',
                'expected_output': 'results logged',
                'has_rollback': False
            }
        ]
    )

    # Execute task
    success = orchestrator.execute_task_with_verification(sample_task)
    logger.info(f"\nTask execution result: {'SUCCESS' if success else 'FAILED'}")
    logger.info(f"Execution stats: {orchestrator.get_execution_stats()}")
