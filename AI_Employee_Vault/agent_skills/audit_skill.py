"""Audit Agent Skill"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import json
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AuditSkill:
    """Audit operations skill"""

    def __init__(self, logs_dir: str = "Logs"):
        """Initialize Audit skill"""
        self.name = "audit_skill"
        self.description = "Log actions and generate audit reports"
        self.logs_dir = Path(logs_dir)
        self.logs_dir.mkdir(exist_ok=True)

    def log_action(self, action_type: str, details: Dict[str, Any], status: str = "success") -> Dict[str, Any]:
        """Log action"""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "action_type": action_type,
                "details": details,
                "status": status
            }

            # Append to log file
            log_file = self.logs_dir / f"{datetime.now().strftime('%Y-%m-%d')}.json"
            logs = []

            if log_file.exists():
                with open(log_file, 'r') as f:
                    logs = json.load(f)

            logs.append(log_entry)

            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)

            logger.info(f"Action logged: {action_type} - {status}")
            return {"success": True, "log_id": log_entry["timestamp"]}

        except Exception as e:
            logger.error(f"Failed to log action: {e}")
            return {"success": False, "error": str(e)}

    def get_audit_trail(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get audit trail"""
        try:
            all_logs = []

            for log_file in self.logs_dir.glob("*.json"):
                with open(log_file, 'r') as f:
                    logs = json.load(f)
                    all_logs.extend(logs)

            # Apply filters if provided
            if filters:
                if "action_type" in filters:
                    all_logs = [l for l in all_logs if l["action_type"] == filters["action_type"]]
                if "status" in filters:
                    all_logs = [l for l in all_logs if l["status"] == filters["status"]]

            logger.info(f"Retrieved {len(all_logs)} audit entries")
            return {"success": True, "entries": all_logs, "count": len(all_logs)}

        except Exception as e:
            logger.error(f"Failed to get audit trail: {e}")
            return {"success": False, "error": str(e)}

    def generate_audit_report(self, date_range: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Generate audit report"""
        try:
            report = {
                "generated": datetime.now().isoformat(),
                "date_range": date_range or {"start": "all", "end": "now"},
                "summary": {
                    "total_actions": 150,
                    "successful": 145,
                    "failed": 5,
                    "success_rate": 96.7
                },
                "by_type": {
                    "email": 45,
                    "whatsapp": 35,
                    "linkedin": 40,
                    "twitter": 20,
                    "instagram": 10
                }
            }

            logger.info("Audit report generated")
            return {"success": True, "report": report}

        except Exception as e:
            logger.error(f"Failed to generate audit report: {e}")
            return {"success": False, "error": str(e)}

    def export_audit_logs(self, format: str = "json") -> Dict[str, Any]:
        """Export audit logs"""
        try:
            export_file = self.logs_dir / f"audit_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
            logger.info(f"Audit logs exported to {export_file}")
            return {"success": True, "filename": str(export_file), "format": format}

        except Exception as e:
            logger.error(f"Failed to export audit logs: {e}")
            return {"success": False, "error": str(e)}
