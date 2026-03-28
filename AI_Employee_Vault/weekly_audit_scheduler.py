"""
Weekly Audit Scheduler
Automatically runs weekly audits and generates CEO briefings
"""

import os
import json
import logging
import schedule
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional
from weekly_audit_generator import WeeklyAuditGenerator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WeeklyAuditScheduler:
    """Schedule and manage weekly audits"""

    def __init__(self):
        """Initialize scheduler"""
        self.generator = WeeklyAuditGenerator()
        self.schedule_file = Path('.audit_schedule.json')
        self.load_schedule()

    def load_schedule(self):
        """Load schedule configuration"""
        try:
            if self.schedule_file.exists():
                with open(self.schedule_file, 'r') as f:
                    self.config = json.load(f)
            else:
                self.config = {
                    'enabled': True,
                    'day': 'friday',
                    'time': '17:00',
                    'timezone': 'UTC',
                    'auto_email': True,
                    'auto_save': True,
                }
                self.save_schedule()
        except Exception as e:
            logger.error(f"Failed to load schedule: {e}")
            self.config = {}

    def save_schedule(self):
        """Save schedule configuration"""
        try:
            with open(self.schedule_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info("Schedule saved")
        except Exception as e:
            logger.error(f"Failed to save schedule: {e}")

    def schedule_weekly_audit(self):
        """Schedule weekly audit"""
        day = self.config.get('day', 'friday').lower()
        time_str = self.config.get('time', '17:00')

        # Schedule based on day
        if day == 'monday':
            schedule.every().monday.at(time_str).do(self.run_audit)
        elif day == 'tuesday':
            schedule.every().tuesday.at(time_str).do(self.run_audit)
        elif day == 'wednesday':
            schedule.every().wednesday.at(time_str).do(self.run_audit)
        elif day == 'thursday':
            schedule.every().thursday.at(time_str).do(self.run_audit)
        elif day == 'friday':
            schedule.every().friday.at(time_str).do(self.run_audit)
        elif day == 'saturday':
            schedule.every().saturday.at(time_str).do(self.run_audit)
        elif day == 'sunday':
            schedule.every().sunday.at(time_str).do(self.run_audit)

        logger.info(f"Weekly audit scheduled for {day} at {time_str}")

    def run_audit(self) -> Dict[str, Any]:
        """Run audit immediately"""
        logger.info("Running weekly audit")

        try:
            # Generate audit
            audit = self.generator.generate_complete_audit()

            # Save audit
            if self.config.get('auto_save', True):
                audit_path = self.generator.save_audit(audit)
                logger.info(f"Audit saved to {audit_path}")

            # Generate CEO briefing
            briefing = self.generator.generate_ceo_briefing(audit)

            # Save briefing
            if self.config.get('auto_save', True):
                briefing_path = self.generator.save_ceo_briefing(briefing)
                logger.info(f"CEO briefing saved to {briefing_path}")

            # Send email if configured
            if self.config.get('auto_email', True):
                self._send_audit_email(audit, briefing)

            # Log audit execution
            self._log_audit_execution(audit, briefing)

            return {
                'status': 'success',
                'audit_id': audit['timestamp'],
                'health': audit['summary']['overall_health'],
                'critical_issues': audit['summary']['critical_issues'],
            }

        except Exception as e:
            logger.error(f"Audit execution failed: {e}")
            return {'status': 'error', 'error': str(e)}

    def _send_audit_email(self, audit: Dict, briefing: Dict):
        """Send audit email to CEO"""
        try:
            from universal_email_sender import UniversalEmailSender

            sender = UniversalEmailSender()

            subject = f"Weekly Audit Report - {datetime.now().strftime('%B %d, %Y')}"

            body = f"""
<html>
<body>
<h2>Weekly Business Audit Report</h2>
<p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

<h3>Executive Summary</h3>
<p>{briefing.get('executive_summary', 'N/A')}</p>

<h3>Key Metrics</h3>
<ul>
<li>Revenue: ${briefing['key_metrics']['revenue']:,.0f}</li>
<li>Profit: ${briefing['key_metrics']['profit']:,.0f}</li>
<li>Pipeline Value: ${briefing['key_metrics']['pipeline_value']:,.0f}</li>
<li>Completion Rate: {briefing['key_metrics']['completion_rate']:.1f}%</li>
</ul>

<h3>Critical Issues</h3>
<ul>
"""
            for issue in briefing.get('critical_issues', []):
                body += f"<li>{issue['issue']}: {issue['recommendation']}</li>"

            body += """
</ul>

<h3>Top Recommendations</h3>
<ul>
"""
            for rec in briefing.get('recommendations', []):
                body += f"<li><strong>{rec['title']}</strong>: {rec['description']}</li>"

            body += """
</ul>

<h3>Next Steps</h3>
<ul>
"""
            for step in briefing.get('next_steps', []):
                body += f"<li>{step}</li>"

            body += """
</ul>

<p>Full audit report available in Audits/ directory</p>
</body>
</html>
"""

            # Send to CEO email
            ceo_email = os.getenv('CEO_EMAIL', 'ceo@agentic-sphere.com')
            sender.send_email(
                to=ceo_email,
                subject=subject,
                body=body,
                html=True
            )

            logger.info(f"Audit email sent to {ceo_email}")

        except Exception as e:
            logger.error(f"Failed to send audit email: {e}")

    def _log_audit_execution(self, audit: Dict, briefing: Dict):
        """Log audit execution"""
        try:
            logs_dir = Path('Logs')
            logs_dir.mkdir(exist_ok=True)

            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'type': 'audit_execution',
                'audit_id': audit['timestamp'],
                'health': audit['summary']['overall_health'],
                'critical_issues': audit['summary']['critical_issues'],
                'action_items': audit['summary']['action_items'],
                'status': 'completed',
            }

            log_file = logs_dir / f"{datetime.now().strftime('%Y-%m-%d')}.json"
            logs = []

            if log_file.exists():
                with open(log_file, 'r') as f:
                    logs = json.load(f)

            logs.append(log_entry)

            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)

            logger.info("Audit execution logged")

        except Exception as e:
            logger.error(f"Failed to log audit execution: {e}")

    def start_scheduler(self):
        """Start the scheduler"""
        logger.info("Starting audit scheduler")

        self.schedule_weekly_audit()

        while True:
            try:
                schedule.run_pending()
                time.sleep(60)
            except KeyboardInterrupt:
                logger.info("Scheduler stopped")
                break
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                time.sleep(60)

    def get_next_audit_time(self) -> Optional[str]:
        """Get next scheduled audit time"""
        try:
            for job in schedule.jobs:
                return job.next_run.isoformat()
        except:
            return None

    def get_audit_history(self, limit: int = 10) -> list:
        """Get recent audit history"""
        try:
            audits_dir = Path('Audits')
            if not audits_dir.exists():
                return []

            audit_files = sorted(
                audits_dir.glob('*.json'),
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )[:limit]

            history = []
            for audit_file in audit_files:
                try:
                    with open(audit_file, 'r') as f:
                        audit = json.load(f)
                        history.append({
                            'timestamp': audit.get('timestamp'),
                            'health': audit.get('summary', {}).get('overall_health'),
                            'critical_issues': audit.get('summary', {}).get('critical_issues'),
                            'file': audit_file.name,
                        })
                except:
                    pass

            return history

        except Exception as e:
            logger.error(f"Failed to get audit history: {e}")
            return []

    def get_audit_status(self) -> Dict[str, Any]:
        """Get current audit status"""
        return {
            'scheduler_enabled': self.config.get('enabled', True),
            'schedule_day': self.config.get('day', 'friday'),
            'schedule_time': self.config.get('time', '17:00'),
            'next_audit': self.get_next_audit_time(),
            'recent_audits': self.get_audit_history(5),
        }


def run_audit_now():
    """Run audit immediately"""
    scheduler = WeeklyAuditScheduler()
    result = scheduler.run_audit()
    print(json.dumps(result, indent=2))
    return result


def start_scheduler():
    """Start the scheduler daemon"""
    scheduler = WeeklyAuditScheduler()
    scheduler.start_scheduler()


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == 'now':
        run_audit_now()
    else:
        start_scheduler()
