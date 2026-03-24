"""
Error Handler - Centralized error handling with recovery strategies
"""

import logging
import time
from typing import Dict, Any, Callable, Optional
from datetime import datetime, timedelta
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ErrorType(Enum):
    """Error types"""
    NETWORK_TIMEOUT = "network_timeout"
    API_RATE_LIMIT = "api_rate_limit"
    AUTH_FAILED = "auth_failed"
    SERVICE_UNAVAILABLE = "service_unavailable"
    INVALID_DATA = "invalid_data"
    DATABASE_ERROR = "database_error"
    UNKNOWN = "unknown"


class RecoveryStrategy(Enum):
    """Recovery strategies"""
    RETRY_WITH_BACKOFF = "retry_with_backoff"
    QUEUE_FOR_LATER = "queue_for_later"
    FALLBACK_SERVICE = "fallback_service"
    SKIP_AND_LOG = "skip_and_log"
    ESCALATE = "escalate"


class ErrorHandler:
    """Centralized error handling with recovery strategies"""

    def __init__(self):
        """Initialize error handler"""
        self.max_retries = 3
        self.backoff_factor = 2
        self.circuit_breakers = {}
        self.error_history = []

    def classify_error(self, error: Exception) -> ErrorType:
        """Classify error type"""
        error_str = str(error).lower()

        if 'timeout' in error_str or 'connection' in error_str:
            return ErrorType.NETWORK_TIMEOUT
        elif 'rate limit' in error_str or '429' in error_str:
            return ErrorType.API_RATE_LIMIT
        elif 'auth' in error_str or '401' in error_str or '403' in error_str:
            return ErrorType.AUTH_FAILED
        elif 'unavailable' in error_str or '503' in error_str:
            return ErrorType.SERVICE_UNAVAILABLE
        elif 'invalid' in error_str or 'validation' in error_str:
            return ErrorType.INVALID_DATA
        elif 'database' in error_str or 'db' in error_str:
            return ErrorType.DATABASE_ERROR
        else:
            return ErrorType.UNKNOWN

    def get_recovery_strategy(self, error_type: ErrorType) -> RecoveryStrategy:
        """Get recovery strategy for error type"""
        strategies = {
            ErrorType.NETWORK_TIMEOUT: RecoveryStrategy.RETRY_WITH_BACKOFF,
            ErrorType.API_RATE_LIMIT: RecoveryStrategy.QUEUE_FOR_LATER,
            ErrorType.AUTH_FAILED: RecoveryStrategy.ESCALATE,
            ErrorType.SERVICE_UNAVAILABLE: RecoveryStrategy.FALLBACK_SERVICE,
            ErrorType.INVALID_DATA: RecoveryStrategy.SKIP_AND_LOG,
            ErrorType.DATABASE_ERROR: RecoveryStrategy.RETRY_WITH_BACKOFF,
            ErrorType.UNKNOWN: RecoveryStrategy.ESCALATE,
        }
        return strategies.get(error_type, RecoveryStrategy.ESCALATE)

    def handle_error(self, error: Exception, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle error with recovery strategy

        Args:
            error: Exception that occurred
            context: Context information

        Returns:
            Recovery action
        """
        error_type = self.classify_error(error)
        strategy = self.get_recovery_strategy(error_type)

        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'error_type': error_type.value,
            'error_message': str(error),
            'strategy': strategy.value,
            'context': context,
        }
        self.error_history.append(log_entry)

        logger.error(f"Error: {error_type.value} - Strategy: {strategy.value}")

        return {
            'error_type': error_type.value,
            'strategy': strategy.value,
            'action': self._get_action(strategy, context),
        }

    def _get_action(self, strategy: RecoveryStrategy, context: Dict) -> Dict[str, Any]:
        """Get action for recovery strategy"""
        if strategy == RecoveryStrategy.RETRY_WITH_BACKOFF:
            return {
                'type': 'retry',
                'max_retries': self.max_retries,
                'backoff_factor': self.backoff_factor,
            }
        elif strategy == RecoveryStrategy.QUEUE_FOR_LATER:
            return {
                'type': 'queue',
                'retry_after_seconds': 300,
            }
        elif strategy == RecoveryStrategy.FALLBACK_SERVICE:
            return {
                'type': 'fallback',
                'fallback_service': context.get('fallback_service'),
            }
        elif strategy == RecoveryStrategy.SKIP_AND_LOG:
            return {
                'type': 'skip',
                'log_error': True,
            }
        else:  # ESCALATE
            return {
                'type': 'escalate',
                'notify_admin': True,
            }

    def retry_with_backoff(self, func: Callable, *args, **kwargs) -> Any:
        """
        Retry function with exponential backoff

        Args:
            func: Function to retry
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Function result
        """
        last_error = None

        for attempt in range(self.max_retries):
            try:
                logger.info(f"Attempt {attempt + 1}/{self.max_retries}")
                return func(*args, **kwargs)
            except Exception as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    wait_time = (self.backoff_factor ** attempt)
                    logger.warning(f"Retry attempt {attempt + 1} failed, waiting {wait_time}s")
                    time.sleep(wait_time)
                else:
                    logger.error(f"All {self.max_retries} attempts failed")

        raise last_error

    def circuit_breaker(self, service_name: str, func: Callable, *args, **kwargs) -> Any:
        """
        Circuit breaker pattern for service calls

        Args:
            service_name: Name of service
            func: Function to call
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Function result
        """
        if service_name not in self.circuit_breakers:
            self.circuit_breakers[service_name] = {
                'state': 'closed',  # closed, open, half_open
                'failures': 0,
                'last_failure_time': None,
                'success_count': 0,
            }

        breaker = self.circuit_breakers[service_name]

        # Check if circuit should be closed
        if breaker['state'] == 'open':
            if datetime.now() - breaker['last_failure_time'] > timedelta(seconds=60):
                logger.info(f"Circuit breaker for {service_name} entering half-open state")
                breaker['state'] = 'half_open'
                breaker['success_count'] = 0
            else:
                raise Exception(f"Circuit breaker for {service_name} is open")

        try:
            result = func(*args, **kwargs)

            # Success
            if breaker['state'] == 'half_open':
                breaker['success_count'] += 1
                if breaker['success_count'] >= 2:
                    logger.info(f"Circuit breaker for {service_name} closed")
                    breaker['state'] = 'closed'
                    breaker['failures'] = 0

            return result

        except Exception as e:
            breaker['failures'] += 1
            breaker['last_failure_time'] = datetime.now()

            if breaker['failures'] >= 3:
                logger.error(f"Circuit breaker for {service_name} opened after {breaker['failures']} failures")
                breaker['state'] = 'open'

            raise e

    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of errors"""
        if not self.error_history:
            return {'total_errors': 0}

        error_types = {}
        for entry in self.error_history:
            error_type = entry['error_type']
            error_types[error_type] = error_types.get(error_type, 0) + 1

        return {
            'total_errors': len(self.error_history),
            'error_types': error_types,
            'recent_errors': self.error_history[-5:],
        }

    def clear_history(self):
        """Clear error history"""
        self.error_history = []
        logger.info("Error history cleared")
