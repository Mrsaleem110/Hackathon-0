#!/usr/bin/env python3
"""
Cloud Health Monitor - Monitors cloud VM health and services
Tracks CPU, memory, disk space, process health, and MCP server status
Sends alerts to Local agent via vault signals
"""

import os
import sys
import json
import psutil
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CloudHealthMonitor:
    """Monitors cloud VM and service health"""

    def __init__(self, vault_path: str = ".", alert_threshold: float = 80.0):
        """
        Initialize health monitor

        Args:
            vault_path: Path to vault directory
            alert_threshold: Percentage threshold for alerts (CPU, memory, disk)
        """
        self.vault_path = Path(vault_path)
        self.alert_threshold = alert_threshold
        self.updates_dir = self.vault_path / "Updates"
        self.logs_dir = self.vault_path / "Logs"

        self.updates_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        # MCP servers to monitor
        self.mcp_servers = {
            "email_mcp": 8070,
            "vault_mcp": 8072,
            "whatsapp_mcp": 8073,
            "odoo_mcp": 8074,
            "twitter_mcp": 8071,
        }

        logger.info("Cloud Health Monitor initialized")

    def check_all(self) -> Dict:
        """
        Run all health checks

        Returns:
            Dictionary with all health check results
        """
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "overall_status": "HEALTHY",
            "checks": {},
            "alerts": [],
        }

        try:
            # 1. Check CPU
            cpu_status = self.check_cpu()
            report["checks"]["cpu"] = cpu_status
            if cpu_status["status"] != "HEALTHY":
                report["alerts"].append(f"CPU: {cpu_status['status']} ({cpu_status['usage']}%)")

            # 2. Check memory
            memory_status = self.check_memory()
            report["checks"]["memory"] = memory_status
            if memory_status["status"] != "HEALTHY":
                report["alerts"].append(f"Memory: {memory_status['status']} ({memory_status['usage']}%)")

            # 3. Check disk space
            disk_status = self.check_disk()
            report["checks"]["disk"] = disk_status
            if disk_status["status"] != "HEALTHY":
                report["alerts"].append(f"Disk: {disk_status['status']} ({disk_status['usage']}%)")

            # 4. Check MCP servers
            mcp_status = self.check_mcp_servers()
            report["checks"]["mcp_servers"] = mcp_status
            for server, status in mcp_status.items():
                if status["status"] != "HEALTHY":
                    report["alerts"].append(f"MCP {server}: {status['status']}")

            # 5. Check cloud agent process
            agent_status = self.check_process("cloud_agent.py")
            report["checks"]["cloud_agent"] = agent_status
            if agent_status["status"] != "RUNNING":
                report["alerts"].append(f"Cloud Agent: {agent_status['status']}")

            # Determine overall status
            if report["alerts"]:
                if any("CRITICAL" in alert for alert in report["alerts"]):
                    report["overall_status"] = "DOWN"
                elif any("DEGRADED" in alert for alert in report["alerts"]):
                    report["overall_status"] = "DEGRADED"
                else:
                    report["overall_status"] = "OPERATIONAL"
            else:
                report["overall_status"] = "HEALTHY"

            # Log report
            self._log_report(report)

            # Write alert signal if needed
            if report["alerts"]:
                self._write_alert_signal(report)

        except Exception as e:
            logger.error(f"Error in health check: {e}")
            report["overall_status"] = "ERROR"
            report["alerts"].append(f"Health check error: {str(e)}")

        return report

    def check_cpu(self) -> Dict:
        """
        Check CPU usage

        Returns:
            Dictionary with CPU status
        """
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()

            status = "HEALTHY"
            if cpu_percent > self.alert_threshold:
                status = "DEGRADED"
            if cpu_percent > 95:
                status = "CRITICAL"

            return {
                "status": status,
                "usage": cpu_percent,
                "cores": cpu_count,
                "threshold": self.alert_threshold,
            }
        except Exception as e:
            logger.error(f"Error checking CPU: {e}")
            return {"status": "ERROR", "error": str(e)}

    def check_memory(self) -> Dict:
        """
        Check memory usage

        Returns:
            Dictionary with memory status
        """
        try:
            memory = psutil.virtual_memory()
            memory_percent = memory.percent

            status = "HEALTHY"
            if memory_percent > self.alert_threshold:
                status = "DEGRADED"
            if memory_percent > 95:
                status = "CRITICAL"

            return {
                "status": status,
                "usage": memory_percent,
                "total_gb": memory.total / (1024 ** 3),
                "available_gb": memory.available / (1024 ** 3),
                "threshold": self.alert_threshold,
            }
        except Exception as e:
            logger.error(f"Error checking memory: {e}")
            return {"status": "ERROR", "error": str(e)}

    def check_disk(self) -> Dict:
        """
        Check disk space

        Returns:
            Dictionary with disk status
        """
        try:
            disk = psutil.disk_usage("/")
            disk_percent = disk.percent

            status = "HEALTHY"
            if disk_percent > self.alert_threshold:
                status = "DEGRADED"
            if disk_percent > 95:
                status = "CRITICAL"

            return {
                "status": status,
                "usage": disk_percent,
                "total_gb": disk.total / (1024 ** 3),
                "free_gb": disk.free / (1024 ** 3),
                "threshold": self.alert_threshold,
            }
        except Exception as e:
            logger.error(f"Error checking disk: {e}")
            return {"status": "ERROR", "error": str(e)}

    def check_mcp_servers(self) -> Dict[str, Dict]:
        """
        Check MCP server health

        Returns:
            Dictionary with status for each MCP server
        """
        results = {}

        for server_name, port in self.mcp_servers.items():
            try:
                # Try to connect to health endpoint
                result = subprocess.run(
                    ["curl", "-s", "-m", "5", f"http://localhost:{port}/health"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )

                if result.returncode == 0:
                    try:
                        health_data = json.loads(result.stdout)
                        status = health_data.get("status", "UNKNOWN")
                    except:
                        status = "HEALTHY" if result.stdout else "UNKNOWN"
                else:
                    status = "DOWN"

                results[server_name] = {
                    "status": status,
                    "port": port,
                    "response_time_ms": 0,
                }

            except subprocess.TimeoutExpired:
                results[server_name] = {
                    "status": "TIMEOUT",
                    "port": port,
                }
            except Exception as e:
                logger.warning(f"Error checking {server_name}: {e}")
                results[server_name] = {
                    "status": "ERROR",
                    "port": port,
                    "error": str(e),
                }

        return results

    def check_process(self, process_name: str) -> Dict:
        """
        Check if a process is running

        Args:
            process_name: Name of process to check

        Returns:
            Dictionary with process status
        """
        try:
            for proc in psutil.process_iter(["pid", "name", "cmdline"]):
                try:
                    if process_name in proc.name() or any(
                        process_name in arg for arg in (proc.info["cmdline"] or [])
                    ):
                        return {
                            "status": "RUNNING",
                            "pid": proc.pid,
                            "name": proc.name(),
                        }
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            return {"status": "NOT_RUNNING", "name": process_name}

        except Exception as e:
            logger.error(f"Error checking process {process_name}: {e}")
            return {"status": "ERROR", "error": str(e)}

    def _log_report(self, report: Dict):
        """Log health report"""
        try:
            today = datetime.utcnow().strftime("%Y-%m-%d")
            log_file = self.logs_dir / f"health_{today}.json"

            logs = []
            if log_file.exists():
                with open(log_file, "r") as f:
                    logs = json.load(f)

            logs.append(report)

            with open(log_file, "w") as f:
                json.dump(logs, f, indent=2)

            logger.info(f"Health report logged to {log_file}")
        except Exception as e:
            logger.error(f"Failed to log health report: {e}")

    def _write_alert_signal(self, report: Dict):
        """Write alert signal to Updates/ for Local agent"""
        try:
            timestamp = datetime.utcnow().isoformat()
            filename = f"signal_alert_{timestamp.replace(':', '-')}.json"
            signal_file = self.updates_dir / filename

            signal_data = {
                "timestamp": timestamp,
                "agent": "cloud",
                "type": "alert",
                "content": {
                    "level": "WARNING" if report["overall_status"] == "DEGRADED" else "CRITICAL",
                    "message": f"Cloud health: {report['overall_status']}",
                    "alerts": report["alerts"],
                    "status": report["overall_status"],
                },
            }

            with open(signal_file, "w") as f:
                json.dump(signal_data, f, indent=2)

            logger.info(f"Alert signal written: {filename}")
        except Exception as e:
            logger.error(f"Failed to write alert signal: {e}")

    def generate_report(self) -> str:
        """
        Generate human-readable health report

        Returns:
            Formatted report string
        """
        report = self.check_all()

        output = []
        output.append("=" * 70)
        output.append("CLOUD HEALTH REPORT")
        output.append("=" * 70)
        output.append(f"Timestamp: {report['timestamp']}")
        output.append(f"Overall Status: {report['overall_status']}")
        output.append("")

        # CPU
        cpu = report["checks"].get("cpu", {})
        output.append(f"CPU: {cpu.get('status', 'UNKNOWN')}")
        output.append(f"  Usage: {cpu.get('usage', 'N/A')}%")
        output.append(f"  Cores: {cpu.get('cores', 'N/A')}")
        output.append("")

        # Memory
        memory = report["checks"].get("memory", {})
        output.append(f"Memory: {memory.get('status', 'UNKNOWN')}")
        output.append(f"  Usage: {memory.get('usage', 'N/A')}%")
        output.append(f"  Total: {memory.get('total_gb', 'N/A'):.1f} GB")
        output.append(f"  Available: {memory.get('available_gb', 'N/A'):.1f} GB")
        output.append("")

        # Disk
        disk = report["checks"].get("disk", {})
        output.append(f"Disk: {disk.get('status', 'UNKNOWN')}")
        output.append(f"  Usage: {disk.get('usage', 'N/A')}%")
        output.append(f"  Total: {disk.get('total_gb', 'N/A'):.1f} GB")
        output.append(f"  Free: {disk.get('free_gb', 'N/A'):.1f} GB")
        output.append("")

        # MCP Servers
        mcp = report["checks"].get("mcp_servers", {})
        output.append("MCP Servers:")
        for server, status in mcp.items():
            output.append(f"  {server}: {status.get('status', 'UNKNOWN')} (port {status.get('port', 'N/A')})")
        output.append("")

        # Cloud Agent
        agent = report["checks"].get("cloud_agent", {})
        output.append(f"Cloud Agent: {agent.get('status', 'UNKNOWN')}")
        if agent.get("pid"):
            output.append(f"  PID: {agent.get('pid')}")
        output.append("")

        # Alerts
        if report["alerts"]:
            output.append("ALERTS:")
            for alert in report["alerts"]:
                output.append(f"  - {alert}")
            output.append("")

        output.append("=" * 70)

        return "\n".join(output)


def main():
    """Demo of cloud health monitor"""
    import sys
    sys.stdout.reconfigure(encoding='utf-8')

    monitor = CloudHealthMonitor(alert_threshold=80.0)

    print("Cloud Health Monitor Demo\n")

    # Run health checks
    print("Running health checks...\n")
    report = monitor.check_all()

    # Display report
    print(monitor.generate_report())

    # Show summary
    print("\nSummary:")
    print(f"  Overall Status: {report['overall_status']}")
    print(f"  Alerts: {len(report['alerts'])}")
    if report['alerts']:
        for alert in report['alerts']:
            print(f"    - {alert}")

    print("\n[OK] Cloud health monitor demo completed!")


if __name__ == "__main__":
    main()
