"""
Quick Start - Weekly Audit and CEO Briefing System
Run audits and generate briefings immediately
"""

import sys
import json
from pathlib import Path
from weekly_audit_generator import WeeklyAuditGenerator
from weekly_audit_scheduler import WeeklyAuditScheduler
from audit_dashboard import AuditDashboard


def print_header(title):
    """Print formatted header"""
    print("\n" + "="*80)
    print(title.center(80))
    print("="*80 + "\n")


def main():
    """Main quick start"""
    print_header("WEEKLY AUDIT & CEO BRIEFING - QUICK START")

    print("🚀 Initializing system...\n")

    # Initialize components
    generator = WeeklyAuditGenerator()
    scheduler = WeeklyAuditScheduler()
    dashboard = AuditDashboard()

    print("✅ System initialized\n")

    # Menu
    while True:
        print("\n" + "-"*80)
        print("MAIN MENU")
        print("-"*80)
        print("1. Run Audit Now")
        print("2. View Dashboard")
        print("3. View Latest Audit")
        print("4. View CEO Briefing")
        print("5. Schedule Weekly Audit")
        print("6. View Audit History")
        print("7. Export Report")
        print("8. Exit")
        print("-"*80)

        choice = input("\nSelect option (1-8): ").strip()

        if choice == '1':
            run_audit_now(generator, scheduler)
        elif choice == '2':
            dashboard.display_dashboard()
        elif choice == '3':
            dashboard.display_latest_audit()
        elif choice == '4':
            dashboard.display_ceo_briefing()
        elif choice == '5':
            schedule_audit(scheduler)
        elif choice == '6':
            view_history(scheduler)
        elif choice == '7':
            export_report(dashboard)
        elif choice == '8':
            print("\n✅ Goodbye!\n")
            break
        else:
            print("❌ Invalid option")


def run_audit_now(generator, scheduler):
    """Run audit immediately"""
    print_header("RUNNING AUDIT")

    print("⏳ Generating audit...\n")

    try:
        # Generate audit
        audit = generator.generate_complete_audit()
        audit_path = generator.save_audit(audit)

        print(f"✅ Audit generated: {audit_path}\n")

        # Generate briefing
        print("⏳ Generating CEO briefing...\n")
        briefing = generator.generate_ceo_briefing(audit)
        briefing_path = generator.save_ceo_briefing(briefing)

        print(f"✅ CEO briefing generated: {briefing_path}\n")

        # Display summary
        summary = audit['summary']
        print("📊 AUDIT SUMMARY")
        print("-"*80)
        print(f"Health Status: {summary['overall_health'].upper()}")
        print(f"Revenue: ${summary['key_metrics']['revenue']:,.0f}")
        print(f"Profit: ${summary['key_metrics']['profit']:,.0f}")
        print(f"Pipeline Value: ${summary['key_metrics']['pipeline_value']:,.0f}")
        print(f"Critical Issues: {summary['critical_issues']}")
        print(f"Action Items: {summary['action_items']}")

        # Log execution
        scheduler._log_audit_execution(audit, briefing)
        print("\n✅ Audit logged successfully")

    except Exception as e:
        print(f"❌ Error: {e}")


def schedule_audit(scheduler):
    """Configure audit schedule"""
    print_header("SCHEDULE WEEKLY AUDIT")

    print("Current Schedule Configuration:")
    print(f"  Day: {scheduler.config.get('day', 'friday')}")
    print(f"  Time: {scheduler.config.get('time', '17:00')}")
    print(f"  Auto-save: {scheduler.config.get('auto_save', True)}")
    print(f"  Auto-email: {scheduler.config.get('auto_email', True)}\n")

    change = input("Change schedule? (y/n): ").strip().lower()

    if change == 'y':
        day = input("Day (monday-sunday): ").strip().lower()
        time_str = input("Time (HH:MM): ").strip()

        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            scheduler.config['day'] = day
            scheduler.config['time'] = time_str
            scheduler.save_schedule()
            print(f"\n✅ Schedule updated: {day} at {time_str}")
        else:
            print("❌ Invalid day")
    else:
        print("✅ Schedule unchanged")


def view_history(scheduler):
    """View audit history"""
    print_header("AUDIT HISTORY")

    history = scheduler.get_audit_history(10)

    if not history:
        print("No audits found")
        return

    print(f"{'#':<3} {'Timestamp':<25} {'Health':<12} {'Critical Issues':<15}")
    print("-"*80)

    for i, audit in enumerate(history, 1):
        health_icon = "🟢" if audit['health'] == 'healthy' else "🟡" if audit['health'] == 'degraded' else "🔴"
        print(f"{i:<3} {audit['timestamp']:<25} {health_icon} {audit['health']:<10} {audit['critical_issues']:<15}")


def export_report(dashboard):
    """Export audit report"""
    print_header("EXPORT REPORT")

    print("Export format:")
    print("1. JSON")
    print("2. Text")

    choice = input("\nSelect format (1-2): ").strip()

    if choice == '1':
        export_file = dashboard.export_audit_report('json')
        print(f"\n✅ Exported to {export_file}")
    elif choice == '2':
        export_file = dashboard.export_audit_report('txt')
        print(f"\n✅ Exported to {export_file}")
    else:
        print("❌ Invalid option")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✅ Exiting...\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)
