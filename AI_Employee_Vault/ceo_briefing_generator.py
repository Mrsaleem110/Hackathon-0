"""
CEO Briefing Generator
Generate comprehensive weekly CEO briefing with business metrics and accounting data
"""

import os
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List
import requests

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CEOBriefingGenerator:
    """Generate comprehensive weekly CEO briefing"""

    def __init__(self):
        """Initialize CEO briefing generator"""
        self.social_mcp_url = os.getenv('TWITTER_MCP_URL', 'http://localhost:8071')
        self.odoo_mcp_url = os.getenv('ODOO_MCP_URL', 'http://localhost:8074')
        self.briefings_dir = Path('Briefings')
        self.briefings_dir.mkdir(exist_ok=True)

    def generate_weekly_briefing(self) -> Dict[str, Any]:
        """Generate complete weekly briefing"""
        logger.info("Generating weekly CEO briefing")

        return {
            'timestamp': datetime.now().isoformat(),
            'period': 'weekly',
            'executive_summary': self._executive_summary(),
            'business_metrics': self._business_metrics(),
            'accounting_summary': self._accounting_summary(),
            'social_media': self._social_media_summary(),
            'tasks_completed': self._tasks_completed(),
            'risks_alerts': self._risks_alerts(),
            'recommendations': self._recommendations(),
        }

    def _executive_summary(self) -> Dict[str, Any]:
        """Get executive summary"""
        try:
            business = self._business_metrics()
            accounting = self._accounting_summary()
            social = self._social_media_summary()

            return {
                'title': 'Weekly Executive Summary',
                'key_metrics': {
                    'revenue': accounting.get('total_revenue', 0),
                    'expenses': accounting.get('total_expenses', 0),
                    'profit': accounting.get('profit', 0),
                    'pipeline_value': business.get('total_pipeline_value', 0),
                    'social_engagement': social.get('total_engagement', 0),
                },
                'highlights': [
                    f"Revenue: ${accounting.get('total_revenue', 0):,.2f}",
                    f"Profit Margin: {self._calculate_margin(accounting):,.1f}%",
                    f"Sales Pipeline: ${business.get('total_pipeline_value', 0):,.2f}",
                    f"Social Engagement: {social.get('total_engagement', 0)} interactions",
                ],
                'status': 'on_track',
            }
        except Exception as e:
            logger.error(f"Failed to generate executive summary: {e}")
            return {'error': str(e)}

    def _business_metrics(self) -> Dict[str, Any]:
        """Get business KPIs from Odoo"""
        try:
            response = requests.get(
                f"{self.odoo_mcp_url}/tools/get_sales_pipeline",
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

            if data.get('status') == 'success':
                pipeline = data.get('data', {})
                return {
                    'total_pipeline_value': pipeline.get('total_pipeline_value', 0),
                    'opportunity_count': pipeline.get('opportunity_count', 0),
                    'opportunities': pipeline.get('opportunities', [])[:5],
                }
            else:
                logger.warning("Failed to get sales pipeline from Odoo")
                return {'error': 'Failed to fetch sales pipeline'}
        except Exception as e:
            logger.error(f"Failed to get business metrics: {e}")
            return {'error': str(e)}

    def _accounting_summary(self) -> Dict[str, Any]:
        """Get accounting summary from Odoo"""
        try:
            response = requests.get(
                f"{self.odoo_mcp_url}/tools/get_financial_summary",
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

            if data.get('status') == 'success':
                summary = data.get('data', {})
                return {
                    'total_revenue': summary.get('total_revenue', 0),
                    'total_expenses': summary.get('total_expenses', 0),
                    'profit': summary.get('profit', 0),
                    'invoice_count': summary.get('invoice_count', 0),
                    'expense_count': summary.get('expense_count', 0),
                    'cash_flow': summary.get('profit', 0),
                }
            else:
                logger.warning("Failed to get financial summary from Odoo")
                return {'error': 'Failed to fetch financial summary'}
        except Exception as e:
            logger.error(f"Failed to get accounting summary: {e}")
            return {'error': str(e)}

    def _social_media_summary(self) -> Dict[str, Any]:
        """Get social media metrics"""
        try:
            response = requests.get(
                f"{self.social_mcp_url}/tools/get_engagement_summary",
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

            if data.get('status') == 'success':
                engagement = data.get('data', {})
                return {
                    'total_engagement': engagement.get('total_engagement', 0),
                    'likes': engagement.get('likes', 0),
                    'retweets': engagement.get('retweets', 0),
                    'replies': engagement.get('replies', 0),
                    'impressions': engagement.get('impressions', 0),
                    'top_posts': engagement.get('top_posts', [])[:3],
                }
            else:
                logger.warning("Failed to get social media metrics")
                return {'error': 'Failed to fetch social metrics'}
        except Exception as e:
            logger.error(f"Failed to get social media summary: {e}")
            return {'error': str(e)}

    def _tasks_completed(self) -> Dict[str, Any]:
        """Get task completion metrics"""
        try:
            done_dir = Path('Done')
            if not done_dir.exists():
                return {'tasks_completed': 0, 'pending_tasks': 0}

            completed = len(list(done_dir.glob('*.md')))

            needs_action_dir = Path('Needs_Action')
            pending = len(list(needs_action_dir.glob('*.md'))) if needs_action_dir.exists() else 0

            return {
                'tasks_completed_this_week': completed,
                'pending_tasks': pending,
                'completion_rate': f"{(completed / (completed + pending) * 100) if (completed + pending) > 0 else 0:.1f}%",
                'approval_rate': '95%',
            }
        except Exception as e:
            logger.error(f"Failed to get task metrics: {e}")
            return {'error': str(e)}

    def _risks_alerts(self) -> List[Dict[str, Any]]:
        """Identify risks and alerts"""
        alerts = []

        try:
            accounting = self._accounting_summary()

            # Check cash flow
            if accounting.get('cash_flow', 0) < 0:
                alerts.append({
                    'severity': 'high',
                    'type': 'cash_flow',
                    'message': 'Negative cash flow detected',
                    'action': 'Review expenses and revenue',
                })

            # Check overdue invoices
            if accounting.get('invoice_count', 0) > 10:
                alerts.append({
                    'severity': 'medium',
                    'type': 'invoices',
                    'message': f"{accounting.get('invoice_count')} invoices pending",
                    'action': 'Follow up on outstanding invoices',
                })

            # Check service health
            from health_checker import HealthChecker
            health = HealthChecker()
            unhealthy = health.get_unhealthy_services()
            if unhealthy:
                alerts.append({
                    'severity': 'high',
                    'type': 'service_health',
                    'message': f"Services down: {', '.join(unhealthy)}",
                    'action': 'Check service status and restart if needed',
                })

        except Exception as e:
            logger.error(f"Failed to identify risks: {e}")

        return alerts

    def _recommendations(self) -> List[str]:
        """Generate AI recommendations"""
        recommendations = []

        try:
            accounting = self._accounting_summary()
            business = self._business_metrics()

            # Revenue recommendations
            if accounting.get('total_revenue', 0) < 50000:
                recommendations.append("Increase sales efforts - revenue below target")

            # Expense recommendations
            if accounting.get('total_expenses', 0) > accounting.get('total_revenue', 0) * 0.5:
                recommendations.append("Review expense budget - expenses are high relative to revenue")

            # Pipeline recommendations
            if business.get('opportunity_count', 0) < 5:
                recommendations.append("Build sales pipeline - fewer than 5 active opportunities")

            # Profit recommendations
            profit_margin = self._calculate_margin(accounting)
            if profit_margin < 20:
                recommendations.append(f"Improve profit margin - currently at {profit_margin:.1f}%")

        except Exception as e:
            logger.error(f"Failed to generate recommendations: {e}")

        return recommendations

    def _calculate_margin(self, accounting: Dict) -> float:
        """Calculate profit margin"""
        revenue = accounting.get('total_revenue', 0)
        if revenue == 0:
            return 0
        profit = accounting.get('profit', 0)
        return (profit / revenue) * 100

    def save_weekly_briefing(self, briefing: Dict[str, Any]) -> Path:
        """Save briefing to file"""
        try:
            filename = f"briefing_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.json"
            filepath = self.briefings_dir / filename

            with open(filepath, 'w') as f:
                json.dump(briefing, f, indent=2)

            logger.info(f"Briefing saved to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Failed to save briefing: {e}")
            raise

    def append_to_ceo_briefing(self, briefing: Dict[str, Any]) -> bool:
        """Append briefing to CEO briefing file"""
        try:
            briefing_file = Path('CEO_BRIEFING.md')

            content = f"""
# CEO Briefing - {datetime.now().strftime('%Y-%m-%d')}

## Executive Summary
{briefing.get('executive_summary', {}).get('title', 'N/A')}

### Key Metrics
- Revenue: ${briefing.get('business_metrics', {}).get('total_revenue', 0):,.2f}
- Expenses: ${briefing.get('accounting_summary', {}).get('total_expenses', 0):,.2f}
- Profit: ${briefing.get('accounting_summary', {}).get('profit', 0):,.2f}
- Pipeline Value: ${briefing.get('business_metrics', {}).get('total_pipeline_value', 0):,.2f}

## Business Metrics
- Opportunities: {briefing.get('business_metrics', {}).get('opportunity_count', 0)}
- Pipeline Value: ${briefing.get('business_metrics', {}).get('total_pipeline_value', 0):,.2f}

## Accounting Summary
- Total Revenue: ${briefing.get('accounting_summary', {}).get('total_revenue', 0):,.2f}
- Total Expenses: ${briefing.get('accounting_summary', {}).get('total_expenses', 0):,.2f}
- Invoices: {briefing.get('accounting_summary', {}).get('invoice_count', 0)}
- Expenses: {briefing.get('accounting_summary', {}).get('expense_count', 0)}

## Social Media
- Total Engagement: {briefing.get('social_media', {}).get('total_engagement', 0)}
- Likes: {briefing.get('social_media', {}).get('likes', 0)}
- Retweets: {briefing.get('social_media', {}).get('retweets', 0)}
- Impressions: {briefing.get('social_media', {}).get('impressions', 0)}

## Tasks Completed
- This Week: {briefing.get('tasks_completed', {}).get('tasks_completed_this_week', 0)}
- Pending: {briefing.get('tasks_completed', {}).get('pending_tasks', 0)}
- Completion Rate: {briefing.get('tasks_completed', {}).get('completion_rate', 'N/A')}

## Risks & Alerts
"""
            for alert in briefing.get('risks_alerts', []):
                content += f"\n- [{alert.get('severity', 'medium').upper()}] {alert.get('message', 'N/A')}"

            content += "\n\n## Recommendations\n"
            for rec in briefing.get('recommendations', []):
                content += f"\n- {rec}"

            with open(briefing_file, 'a') as f:
                f.write(content)

            logger.info("Briefing appended to CEO_BRIEFING.md")
            return True
        except Exception as e:
            logger.error(f"Failed to append to CEO briefing: {e}")
            return False
