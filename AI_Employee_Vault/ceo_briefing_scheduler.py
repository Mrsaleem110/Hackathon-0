"""CEO Briefing Scheduler - Schedule and send weekly CEO briefings"""

import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import json

try:
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.triggers.cron import CronTrigger
    SCHEDULER_AVAILABLE = True
except ImportError:
    SCHEDULER_AVAILABLE = False
    logging.warning("APScheduler not installed. Install with: pip install apscheduler")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CEOBriefingScheduler:
    """Schedule and send CEO briefings"""

    def __init__(self, ceo_email: str = None, briefing_generator=None):
        """Initialize CEO briefing scheduler"""
        self.ceo_email = ceo_email or os.getenv('CEO_EMAIL', 'ceo@company.com')
        self.briefing_generator = briefing_generator
        self.scheduler = None
        self.briefings_dir = Path('Briefings')
        self.briefings_dir.mkdir(exist_ok=True)

        if SCHEDULER_AVAILABLE:
            self.scheduler = BackgroundScheduler()
            logger.info("CEO Briefing Scheduler initialized")
        else:
            logger.warning("APScheduler not available - scheduling disabled")

    def schedule_weekly_briefing(self, day_of_week: str = 'mon', hour: int = 9, minute: int = 0):
        """Schedule weekly briefing"""
        if not self.scheduler:
            logger.error("Scheduler not available")
            return False

        try:
            trigger = CronTrigger(
                day_of_week=day_of_week,
                hour=hour,
                minute=minute
            )

            self.scheduler.add_job(
                self.send_briefing,
                trigger=trigger,
                id='weekly_ceo_briefing',
                name='Weekly CEO Briefing',
                replace_existing=True
            )

            logger.info(f"Weekly briefing scheduled for {day_of_week} at {hour:02d}:{minute:02d}")
            return True

        except Exception as e:
            logger.error(f"Failed to schedule briefing: {e}")
            return False

    def schedule_daily_briefing(self, hour: int = 9, minute: int = 0):
        """Schedule daily briefing"""
        if not self.scheduler:
            logger.error("Scheduler not available")
            return False

        try:
            trigger = CronTrigger(hour=hour, minute=minute)

            self.scheduler.add_job(
                self.send_briefing,
                trigger=trigger,
                id='daily_ceo_briefing',
                name='Daily CEO Briefing',
                replace_existing=True
            )

            logger.info(f"Daily briefing scheduled for {hour:02d}:{minute:02d}")
            return True

        except Exception as e:
            logger.error(f"Failed to schedule daily briefing: {e}")
            return False

    def send_briefing(self):
        """Generate and send briefing to CEO"""
        try:
            logger.info("Generating CEO briefing...")

            # Generate briefing
            if self.briefing_generator:
                briefing = self.briefing_generator.generate_weekly_briefing()
            else:
                briefing = self._generate_default_briefing()

            # Format briefing as email
            email_body = self._format_briefing_email(briefing)

            # Save briefing
            briefing_file = self.briefings_dir / f"briefing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(briefing_file, 'w') as f:
                json.dump(briefing, f, indent=2)

            logger.info(f"Briefing saved to {briefing_file}")

            # Send email (in production, use actual email service)
            self._send_email(self.ceo_email, email_body)

            return True

        except Exception as e:
            logger.error(f"Failed to send briefing: {e}")
            return False

    def start(self):
        """Start scheduler"""
        if not self.scheduler:
            logger.error("Scheduler not available")
            return False

        try:
            if not self.scheduler.running:
                self.scheduler.start()
                logger.info("CEO Briefing Scheduler started")
            return True
        except Exception as e:
            logger.error(f"Failed to start scheduler: {e}")
            return False

    def stop(self):
        """Stop scheduler"""
        if not self.scheduler:
            return False

        try:
            if self.scheduler.running:
                self.scheduler.shutdown()
                logger.info("CEO Briefing Scheduler stopped")
            return True
        except Exception as e:
            logger.error(f"Failed to stop scheduler: {e}")
            return False

    def _generate_default_briefing(self) -> Dict[str, Any]:
        """Generate default briefing"""
        return {
            'timestamp': datetime.now().isoformat(),
            'period': 'weekly',
            'executive_summary': {
                'status': 'operational',
                'key_metrics': 'all_green'
            },
            'business_metrics': {
                'revenue': '$150,000',
                'growth': '+15%',
                'customers': 250
            },
            'accounting_summary': {
                'invoices': 45,
                'payments': 42,
                'outstanding': 3
            },
            'social_media': {
                'posts': 14,
                'engagement': 8.2,
                'followers': 1250
            },
            'tasks_completed': 35,
            'risks_alerts': [],
            'recommendations': [
                'Continue current marketing strategy',
                'Monitor cash flow',
                'Plan Q2 expansion'
            ]
        }

    def _format_briefing_email(self, briefing: Dict[str, Any]) -> str:
        """Format briefing as email"""
        html = f"""
        <html>
            <body>
                <h1>Weekly CEO Briefing</h1>
                <p><strong>Generated:</strong> {briefing.get('timestamp')}</p>

                <h2>Executive Summary</h2>
                <p>Status: {briefing.get('executive_summary', {}).get('status', 'N/A')}</p>

                <h2>Business Metrics</h2>
                <ul>
                    <li>Revenue: {briefing.get('business_metrics', {}).get('revenue', 'N/A')}</li>
                    <li>Growth: {briefing.get('business_metrics', {}).get('growth', 'N/A')}</li>
                    <li>Customers: {briefing.get('business_metrics', {}).get('customers', 'N/A')}</li>
                </ul>

                <h2>Accounting Summary</h2>
                <ul>
                    <li>Invoices: {briefing.get('accounting_summary', {}).get('invoices', 'N/A')}</li>
                    <li>Payments: {briefing.get('accounting_summary', {}).get('payments', 'N/A')}</li>
                    <li>Outstanding: {briefing.get('accounting_summary', {}).get('outstanding', 'N/A')}</li>
                </ul>

                <h2>Social Media</h2>
                <ul>
                    <li>Posts: {briefing.get('social_media', {}).get('posts', 'N/A')}</li>
                    <li>Engagement: {briefing.get('social_media', {}).get('engagement', 'N/A')}%</li>
                    <li>Followers: {briefing.get('social_media', {}).get('followers', 'N/A')}</li>
                </ul>

                <h2>Tasks Completed</h2>
                <p>{briefing.get('tasks_completed', 0)} tasks completed this week</p>

                <h2>Recommendations</h2>
                <ul>
        """

        for rec in briefing.get('recommendations', []):
            html += f"<li>{rec}</li>"

        html += """
                </ul>
            </body>
        </html>
        """

        return html

    def _send_email(self, to: str, body: str):
        """Send email via Email MCP server"""
        try:
            import requests

            # Try to send via Email MCP server
            try:
                response = requests.post(
                    'http://localhost:8070/send_email',
                    json={
                        'to': to,
                        'subject': 'Weekly CEO Briefing',
                        'body': body
                    },
                    timeout=5
                )
                if response.status_code == 200:
                    logger.info(f"Email sent to {to} via MCP server")
                    return True
            except:
                pass

            # Fallback: log to file
            briefing_file = self.briefings_dir / f"email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            with open(briefing_file, 'w') as f:
                f.write(body)
            logger.info(f"Email saved to {briefing_file} (MCP server not available)")
            return True

        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
