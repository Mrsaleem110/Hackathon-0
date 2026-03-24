"""
Degradation Manager - Manage graceful service degradation
"""

import logging
from typing import Dict, Optional
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DegradationManager:
    """Manage graceful service degradation"""

    def __init__(self):
        """Initialize degradation manager"""
        self.degraded_services = set()
        self.fallback_services = {
            'twitter': 'linkedin',
            'instagram': 'facebook',
            'odoo': 'local_cache',
            'gmail': 'local_queue',
        }
        self.degradation_history = []

    def mark_service_degraded(self, service: str):
        """
        Mark service as degraded

        Args:
            service: Service name
        """
        if service not in self.degraded_services:
            self.degraded_services.add(service)
            logger.warning(f"Service marked as degraded: {service}")

            self.degradation_history.append({
                'timestamp': datetime.now().isoformat(),
                'service': service,
                'event': 'degraded',
            })

    def mark_service_recovered(self, service: str):
        """
        Mark service as recovered

        Args:
            service: Service name
        """
        if service in self.degraded_services:
            self.degraded_services.remove(service)
            logger.info(f"Service recovered: {service}")

            self.degradation_history.append({
                'timestamp': datetime.now().isoformat(),
                'service': service,
                'event': 'recovered',
            })

    def get_available_service(self, primary: str) -> str:
        """
        Get available service (primary or fallback)

        Args:
            primary: Primary service name

        Returns:
            Available service name
        """
        if primary not in self.degraded_services:
            return primary

        fallback = self.fallback_services.get(primary)
        if fallback:
            logger.info(f"Using fallback service {fallback} for {primary}")
            return fallback

        logger.warning(f"No fallback available for {primary}")
        return primary

    def execute_with_fallback(self, action: Dict) -> Dict:
        """
        Execute action with fallback if primary fails

        Args:
            action: Action dict with 'service' and 'operation' keys

        Returns:
            Execution result
        """
        primary_service = action.get('service')
        operation = action.get('operation')

        try:
            # Try primary service
            logger.info(f"Executing {operation} on {primary_service}")
            result = self._execute_on_service(primary_service, operation, action)
            return result

        except Exception as e:
            logger.error(f"Primary service {primary_service} failed: {e}")
            self.mark_service_degraded(primary_service)

            # Try fallback service
            fallback = self.fallback_services.get(primary_service)
            if fallback:
                try:
                    logger.info(f"Executing {operation} on fallback service {fallback}")
                    result = self._execute_on_service(fallback, operation, action)
                    return result
                except Exception as e2:
                    logger.error(f"Fallback service {fallback} also failed: {e2}")
                    return {
                        'status': 'failed',
                        'error': f"Both {primary_service} and {fallback} failed",
                        'primary_error': str(e),
                        'fallback_error': str(e2),
                    }
            else:
                return {
                    'status': 'failed',
                    'error': f"Primary service {primary_service} failed and no fallback available",
                    'error_details': str(e),
                }

    def _execute_on_service(self, service: str, operation: str, action: Dict) -> Dict:
        """Execute operation on service"""
        # This would be implemented based on actual service APIs
        # For now, return a placeholder
        return {
            'status': 'success',
            'service': service,
            'operation': operation,
        }

    def is_service_degraded(self, service: str) -> bool:
        """Check if service is degraded"""
        return service in self.degraded_services

    def get_degraded_services(self) -> list:
        """Get list of degraded services"""
        return list(self.degraded_services)

    def get_degradation_status(self) -> Dict:
        """Get degradation status"""
        return {
            'timestamp': datetime.now().isoformat(),
            'degraded_services': list(self.degraded_services),
            'total_degraded': len(self.degraded_services),
            'fallback_services': self.fallback_services,
            'recent_events': self.degradation_history[-10:],
        }

    def clear_history(self):
        """Clear degradation history"""
        self.degradation_history = []
        logger.info("Degradation history cleared")
