"""
Health Checker - Monitor health of all services
"""

import logging
import requests
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ServiceStatus(Enum):
    """Service status"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    DOWN = "down"
    UNKNOWN = "unknown"


class HealthChecker:
    """Monitor health of all services"""

    def __init__(self):
        """Initialize health checker"""
        self.services = {
            'gmail': 'http://localhost:8070/health',
            'twitter': 'http://localhost:8071/health',
            'instagram': 'http://localhost:8072/health',
            'facebook': 'http://localhost:8073/health',
            'odoo': 'http://localhost:8074/health',
        }
        self.status_cache = {}
        self.last_check_time = {}

    def check_all_services(self) -> Dict[str, Dict]:
        """
        Check health of all services

        Args:
            None

        Returns:
            Status dict for all services
        """
        results = {}

        for service_name, url in self.services.items():
            results[service_name] = self.check_service(service_name, url)

        return results

    def check_service(self, service_name: str, url: str) -> Dict:
        """
        Check health of single service

        Args:
            service_name: Name of service
            url: Health check URL

        Returns:
            Service status dict
        """
        start_time = datetime.now()

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()

            response_time = (datetime.now() - start_time).total_seconds()

            status = {
                'status': ServiceStatus.HEALTHY.value,
                'response_time_ms': response_time * 1000,
                'last_check': datetime.now().isoformat(),
                'error': None,
            }

            self.status_cache[service_name] = status
            self.last_check_time[service_name] = datetime.now()

            logger.info(f"{service_name}: HEALTHY ({response_time*1000:.0f}ms)")
            return status

        except requests.Timeout:
            status = {
                'status': ServiceStatus.DEGRADED.value,
                'response_time_ms': 5000,
                'last_check': datetime.now().isoformat(),
                'error': 'Timeout',
            }
            logger.warning(f"{service_name}: DEGRADED (Timeout)")
            return status

        except requests.ConnectionError:
            status = {
                'status': ServiceStatus.DOWN.value,
                'response_time_ms': None,
                'last_check': datetime.now().isoformat(),
                'error': 'Connection refused',
            }
            logger.error(f"{service_name}: DOWN (Connection refused)")
            return status

        except Exception as e:
            status = {
                'status': ServiceStatus.DOWN.value,
                'response_time_ms': None,
                'last_check': datetime.now().isoformat(),
                'error': str(e),
            }
            logger.error(f"{service_name}: DOWN ({str(e)})")
            return status

    def get_service_status(self, service_name: str) -> Dict:
        """
        Get detailed status for service

        Args:
            service_name: Name of service

        Returns:
            Detailed status dict
        """
        if service_name not in self.services:
            return {'error': f'Service {service_name} not found'}

        url = self.services[service_name]
        status = self.check_service(service_name, url)

        return {
            'service': service_name,
            'status': status['status'],
            'response_time_ms': status['response_time_ms'],
            'last_check': status['last_check'],
            'error': status['error'],
        }

    def get_overall_status(self) -> Dict:
        """Get overall system status"""
        all_status = self.check_all_services()

        healthy_count = sum(1 for s in all_status.values() if s['status'] == ServiceStatus.HEALTHY.value)
        degraded_count = sum(1 for s in all_status.values() if s['status'] == ServiceStatus.DEGRADED.value)
        down_count = sum(1 for s in all_status.values() if s['status'] == ServiceStatus.DOWN.value)

        overall_status = ServiceStatus.HEALTHY.value
        if down_count > 0:
            overall_status = ServiceStatus.DOWN.value
        elif degraded_count > 0:
            overall_status = ServiceStatus.DEGRADED.value

        return {
            'overall_status': overall_status,
            'healthy': healthy_count,
            'degraded': degraded_count,
            'down': down_count,
            'total': len(self.services),
            'services': all_status,
            'timestamp': datetime.now().isoformat(),
        }

    def is_service_healthy(self, service_name: str) -> bool:
        """Check if service is healthy"""
        if service_name not in self.services:
            return False

        status = self.check_service(service_name, self.services[service_name])
        return status['status'] == ServiceStatus.HEALTHY.value

    def get_unhealthy_services(self) -> List[str]:
        """Get list of unhealthy services"""
        all_status = self.check_all_services()
        return [
            name for name, status in all_status.items()
            if status['status'] != ServiceStatus.HEALTHY.value
        ]

    def get_health_report(self) -> Dict:
        """Get comprehensive health report"""
        overall = self.get_overall_status()
        unhealthy = self.get_unhealthy_services()

        return {
            'timestamp': datetime.now().isoformat(),
            'overall_status': overall['overall_status'],
            'summary': {
                'healthy': overall['healthy'],
                'degraded': overall['degraded'],
                'down': overall['down'],
                'total': overall['total'],
            },
            'unhealthy_services': unhealthy,
            'services': overall['services'],
            'recommendations': self._get_recommendations(unhealthy),
        }

    def _get_recommendations(self, unhealthy_services: List[str]) -> List[str]:
        """Get recommendations based on unhealthy services"""
        recommendations = []

        if not unhealthy_services:
            recommendations.append("All services are healthy")
            return recommendations

        for service in unhealthy_services:
            if service == 'odoo':
                recommendations.append("Check Odoo server is running on port 8074")
            elif service == 'twitter':
                recommendations.append("Check Twitter MCP server is running on port 8071")
            elif service == 'instagram':
                recommendations.append("Check Instagram MCP server is running on port 8072")
            elif service == 'facebook':
                recommendations.append("Check Facebook MCP server is running on port 8073")
            elif service == 'gmail':
                recommendations.append("Check Gmail MCP server is running on port 8070")

        return recommendations
