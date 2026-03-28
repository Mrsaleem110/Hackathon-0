"""
Weekly Audit Dashboard
Real-time audit monitoring and reporting
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
from weekly_audit_scheduler import WeeklyAuditScheduler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AuditDashboard:
    """Display and manage audit dashboard"""

    def __init__(self):
        """Initialize dashboard"""
        self.scheduler = WeeklyAuditScheduler()
        self.audits_dir = Path('Audits')
        self.briefings_dir = Path('Briefings')

    def display_dashboard(self):
        """Display audit dashboard"""
        status = self.scheduler.get_audit_status()

        print("\n" + "="*80)
        print("WEEKLY AUDIT DASHBOARD".center(80))
        print("="*80)

        # Scheduler status
        print("\n📅 SCHEDULER STATUS")
        print("-" * 80)
        print(f"Status: {'🟢 ENABLED' if status['scheduler_enabled'] else '🔴 DISABLED'}")
        print(f"Schedule: Every {status['schedule_day'].upper()} at {status['schedule_time']}")
        print(f"Next Audit: {status['next_audit'] or 'Not scheduled'}")

        # Recent audits
        print("\n📊 RECENT AUDITS")
        print("-" * 80)
        if status['recent_audits']:
            for i, audit in enumerate(status['recent_audits'], 1):
                health_icon = self._get_health_icon(audit['health'])
                print(f"{i}. {audit['timestamp']}")
                print(f"   Health: {health_icon} {audit['health'].upper()}")
                print(f"   Critical Issues: {audit['critical_issues']}")
                print(f"   File: {audit['file']}")
        else:
            print("No audits found")

        print("\n" + "="*80)

    def display_latest_audit(self):
        """Display latest audit details"""
        latest = self._get_latest_audit()
        if not latest:
            print("No audits found")
            return

        audit_data, audit_file = latest

        print("\n" + "="*80)
        print(f"AUDIT REPORT - {audit_data['timestamp']}".center(80))
        print("="*80)

        # Summary
        summary = audit_data.get('summary', {})
        print("\n📈 EXECUTIVE SUMMARY")
        print("-" * 80)
        print(f"Overall Health: {self._get_health_icon(summary['overall_health'])} {summary['overall_health'].upper()}")
        print(f"Revenue: ${summary['key_metrics']['revenue']:,.0f}")
        print(f"Profit: ${summary['key_metrics']['profit']:,.0f}")
        print(f"Pipeline Value: ${summary['key_metrics']['pipeline_value']:,.0f}")
        print(f"Completion Rate: {summary['key_metrics']['completion_rate']:.1f}%")
        print(f"Critical Issues: {summary['critical_issues']}")
        print(f"Action Items: {summary['action_items']}")

        # Financial Audit
        financial = audit_data['sections'].get('financial_audit', {})
        if financial.get('status') == 'completed':
            print("\n💰 FINANCIAL AUDIT")
            print("-" * 80)
            print(f"Total Revenue: ${financial['revenue']['total']:,.0f}")
            print(f"Revenue Trend: {financial['revenue']['trend']}")
            print(f"Total Expenses: ${financial['expenses']['total']:,.0f}")
            print(f"Expense Trend: {financial['expenses']['trend']}")
            print(f"Gross Profit: ${financial['profitability']['gross_profit']:,.0f}")
            print(f"Profit Margin: {financial['profitability']['profit_margin']:.1f}%")
            print(f"Cash Flow: ${financial['cash_flow']['current']:,.0f}")
            print(f"Cash Health: {financial['cash_flow']['health'].upper()}")
            print(f"Invoices - Total: {financial['invoices']['total_count']}, "
                  f"Paid: {financial['invoices']['paid']}, "
                  f"Overdue: {financial['invoices']['overdue']}")

        # Operational Audit
        operational = audit_data['sections'].get('operational_audit', {})
        if operational.get('status') == 'completed':
            print("\n🎯 OPERATIONAL AUDIT")
            print("-" * 80)
            print(f"Pipeline Value: ${operational['sales_pipeline']['total_value']:,.0f}")
            print(f"Opportunities: {operational['sales_pipeline']['opportunity_count']}")
            print(f"Conversion Rate: {operational['sales_pipeline']['conversion_rate']:.1f}%")
            print(f"Avg Deal Size: ${operational['sales_pipeline']['avg_deal_size']:,.0f}")
            print(f"Sales Cycle: {operational['sales_pipeline']['sales_cycle_days']} days")
            print(f"Tasks Completed: {operational['task_completion']['completed_this_week']}")
            print(f"Pending Tasks: {operational['task_completion']['pending']}")
            print(f"Completion Rate: {operational['task_completion']['completion_rate']:.1f}%")
            print(f"Approval Rate: {operational['task_completion']['approval_rate']:.1f}%")

        # Compliance Audit
        compliance = audit_data['sections'].get('compliance_audit', {})
        if compliance.get('status') == 'completed':
            print("\n🔒 COMPLIANCE AUDIT")
            print("-" * 80)
            print(f"Total Actions: {compliance['audit_trail']['total_actions']}")
            print(f"Success Rate: {compliance['audit_trail']['success_rate']:.1f}%")
            print(f"Failed Actions: {compliance['audit_trail']['failed_actions']}")
            print(f"Data Integrity Score: {compliance['data_integrity']['integrity_score']:.1f}%")
            print(f"Unauthorized Attempts: {compliance['access_control']['unauthorized_attempts']}")
            print(f"Security Incidents: {compliance['access_control']['security_incidents']}")

        # Performance Metrics
        performance = audit_data['sections'].get('performance_metrics', {})
        print("\n⚡ PERFORMANCE METRICS")
        print("-" * 80)
        print(f"System Uptime: {performance['system_health']['uptime_percentage']:.1f}%")
        print(f"Response Time: {performance['system_health']['response_time_ms']}ms")
        print(f"Error Rate: {performance['system_health']['error_rate']:.2f}%")
        print(f"Healthy Services: {performance['system_health']['services_healthy']}")
        print(f"Social Posts: {performance['social_media']['total_posts']}")
        print(f"Social Engagement: {performance['social_media']['total_engagement']}")
        print(f"Emails Sent: {performance['email_metrics']['emails_sent']}")
        print(f"Email Open Rate: {performance['email_metrics']['open_rate']:.1f}%")

        # Risk Assessment
        risks = audit_data['sections'].get('risk_assessment', {})
        print("\n⚠️  RISK ASSESSMENT")
        print("-" * 80)
        print(f"Total Risks: {risks['total_risks']}")
        print(f"Critical: {risks['critical']}")
        print(f"High: {risks['high']}")
        print(f"Medium: {risks['medium']}")

        if risks.get('risks'):
            print("\nRisks:")
            for risk in risks['risks'][:5]:
                severity_icon = self._get_severity_icon(risk['severity'])
                print(f"  {severity_icon} [{risk['severity'].upper()}] {risk['issue']}")
                print(f"     → {risk['recommendation']}")

        # Recommendations
        recommendations = audit_data['sections'].get('recommendations', [])
        if recommendations:
            print("\n💡 TOP RECOMMENDATIONS")
            print("-" * 80)
            for i, rec in enumerate(recommendations[:5], 1):
                print(f"{i}. {rec['title']} (Priority: {rec['priority'].upper()})")
                print(f"   {rec['description']}")
                print(f"   Expected Impact: {rec['expected_impact']}")

        print("\n" + "="*80)

    def display_ceo_briefing(self):
        """Display CEO briefing"""
        latest_briefing = self._get_latest_briefing()
        if not latest_briefing:
            print("No briefings found")
            return

        briefing_data, briefing_file = latest_briefing

        print("\n" + "="*80)
        print("CEO BRIEFING".center(80))
        print("="*80)

        print(f"\nGenerated: {briefing_data['timestamp']}")

        print("\n📋 EXECUTIVE SUMMARY")
        print("-" * 80)
        print(briefing_data.get('executive_summary', 'N/A'))

        print("\n📊 KEY METRICS")
        print("-" * 80)
        metrics = briefing_data.get('key_metrics', {})
        print(f"Revenue: ${metrics.get('revenue', 0):,.0f}")
        print(f"Profit: ${metrics.get('profit', 0):,.0f}")
        print(f"Pipeline Value: ${metrics.get('pipeline_value', 0):,.0f}")
        print(f"Completion Rate: {metrics.get('completion_rate', 0):.1f}%")

        print("\n🚨 CRITICAL ISSUES")
        print("-" * 80)
        critical = briefing_data.get('critical_issues', [])
        if critical:
            for issue in critical:
                print(f"• {issue['issue']}")
                print(f"  Impact: {issue['impact']}")
                print(f"  Action: {issue['recommendation']}")
        else:
            print("No critical issues")

        print("\n💡 TOP RECOMMENDATIONS")
        print("-" * 80)
        recommendations = briefing_data.get('recommendations', [])
        for i, rec in enumerate(recommendations[:5], 1):
            print(f"{i}. {rec['title']}")
            print(f"   Priority: {rec['priority'].upper()}")
            print(f"   {rec['description']}")

        print("\n📌 NEXT STEPS")
        print("-" * 80)
        next_steps = briefing_data.get('next_steps', [])
        for i, step in enumerate(next_steps, 1):
            print(f"{i}. {step}")

        print("\n" + "="*80)

    def export_audit_report(self, format: str = 'json') -> Path:
        """Export audit report"""
        latest = self._get_latest_audit()
        if not latest:
            print("No audits found")
            return None

        audit_data, _ = latest

        if format == 'json':
            export_file = Path('Audits') / f"audit_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(export_file, 'w') as f:
                json.dump(audit_data, f, indent=2)
        elif format == 'txt':
            export_file = Path('Audits') / f"audit_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(export_file, 'w') as f:
                f.write(self._format_audit_as_text(audit_data))

        logger.info(f"Audit exported to {export_file}")
        return export_file

    def _get_latest_audit(self) -> tuple:
        """Get latest audit file"""
        if not self.audits_dir.exists():
            return None

        audit_files = sorted(
            self.audits_dir.glob('audit_*.json'),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )

        if not audit_files:
            return None

        try:
            with open(audit_files[0], 'r') as f:
                audit_data = json.load(f)
            return audit_data, audit_files[0]
        except:
            return None

    def _get_latest_briefing(self) -> tuple:
        """Get latest briefing file"""
        if not self.briefings_dir.exists():
            return None

        briefing_files = sorted(
            self.briefings_dir.glob('ceo_briefing_*.json'),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )

        if not briefing_files:
            return None

        try:
            with open(briefing_files[0], 'r') as f:
                briefing_data = json.load(f)
            return briefing_data, briefing_files[0]
        except:
            return None

    def _get_health_icon(self, health: str) -> str:
        """Get health status icon"""
        icons = {
            'healthy': '🟢',
            'degraded': '🟡',
            'at_risk': '🔴',
        }
        return icons.get(health, '⚪')

    def _get_severity_icon(self, severity: str) -> str:
        """Get severity icon"""
        icons = {
            'critical': '🔴',
            'high': '🟠',
            'medium': '🟡',
            'low': '🟢',
            'info': '🔵',
        }
        return icons.get(severity, '⚪')

    def _format_audit_as_text(self, audit_data: Dict) -> str:
        """Format audit as text"""
        text = f"WEEKLY AUDIT REPORT\n"
        text += f"Generated: {audit_data['timestamp']}\n"
        text += f"Week Ending: {audit_data['week_ending']}\n\n"

        summary = audit_data.get('summary', {})
        text += f"EXECUTIVE SUMMARY\n"
        text += f"Overall Health: {summary['overall_health']}\n"
        text += f"Revenue: ${summary['key_metrics']['revenue']:,.0f}\n"
        text += f"Profit: ${summary['key_metrics']['profit']:,.0f}\n"
        text += f"Critical Issues: {summary['critical_issues']}\n\n"

        return text


def main():
    """Main CLI"""
    import sys

    dashboard = AuditDashboard()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == 'dashboard':
            dashboard.display_dashboard()
        elif command == 'audit':
            dashboard.display_latest_audit()
        elif command == 'briefing':
            dashboard.display_ceo_briefing()
        elif command == 'export':
            format_type = sys.argv[2] if len(sys.argv) > 2 else 'json'
            export_file = dashboard.export_audit_report(format_type)
            print(f"✅ Exported to {export_file}")
        elif command == 'run':
            result = dashboard.scheduler.run_audit()
            print(json.dumps(result, indent=2))
        else:
            print("Unknown command")
    else:
        dashboard.display_dashboard()


if __name__ == '__main__':
    main()
