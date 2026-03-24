"""
Accounting Skills - Accounting operations for agent
"""

from typing import Dict, Any, List
import logging
from skill import Skill, SkillParameter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CreateInvoiceSkill(Skill):
    """Create invoice in Odoo"""

    def __init__(self):
        super().__init__(
            name='create_invoice',
            description='Create invoice in Odoo accounting system',
            group='accounting',
            version='1.0.0',
        )
        self.parameters = [
            SkillParameter('partner_id', 'number', 'Customer ID', required=True),
            SkillParameter('invoice_lines', 'array', 'Invoice line items', required=True),
            SkillParameter('dry_run', 'boolean', 'Test mode', required=False, default=False),
        ]

    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute invoice creation"""
        try:
            self.validate_parameters(**kwargs)

            partner_id = kwargs.get('partner_id')
            invoice_lines = kwargs.get('invoice_lines')
            dry_run = kwargs.get('dry_run', False)

            logger.info(f"Creating invoice for partner {partner_id}")

            result = self._create_via_odoo_mcp({
                'partner_id': partner_id,
                'invoice_lines': invoice_lines,
                'dry_run': dry_run,
            })

            self.log_execution(kwargs, result)
            return result

        except Exception as e:
            logger.error(f"Failed to create invoice: {e}")
            result = {'status': 'error', 'error': str(e)}
            self.log_execution(kwargs, result)
            return result

    def _create_via_odoo_mcp(self, params: Dict) -> Dict[str, Any]:
        """Create via Odoo MCP server"""
        import requests
        try:
            response = requests.post(
                'http://localhost:8074/tools/create_invoice',
                json=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Odoo MCP error: {e}")
            return {'status': 'error', 'error': str(e)}


class RecordExpenseSkill(Skill):
    """Record expense in Odoo"""

    def __init__(self):
        super().__init__(
            name='record_expense',
            description='Record employee expense in Odoo',
            group='accounting',
            version='1.0.0',
        )
        self.parameters = [
            SkillParameter('employee_id', 'number', 'Employee ID', required=True),
            SkillParameter('amount', 'number', 'Expense amount', required=True),
            SkillParameter('description', 'string', 'Expense description', required=True),
            SkillParameter('dry_run', 'boolean', 'Test mode', required=False, default=False),
        ]

    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute expense recording"""
        try:
            self.validate_parameters(**kwargs)

            employee_id = kwargs.get('employee_id')
            amount = kwargs.get('amount')
            description = kwargs.get('description')
            dry_run = kwargs.get('dry_run', False)

            logger.info(f"Recording expense for employee {employee_id}: ${amount}")

            result = self._record_via_odoo_mcp({
                'employee_id': employee_id,
                'amount': amount,
                'description': description,
                'dry_run': dry_run,
            })

            self.log_execution(kwargs, result)
            return result

        except Exception as e:
            logger.error(f"Failed to record expense: {e}")
            result = {'status': 'error', 'error': str(e)}
            self.log_execution(kwargs, result)
            return result

    def _record_via_odoo_mcp(self, params: Dict) -> Dict[str, Any]:
        """Record via Odoo MCP server"""
        import requests
        try:
            response = requests.post(
                'http://localhost:8074/tools/record_expense',
                json=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Odoo MCP error: {e}")
            return {'status': 'error', 'error': str(e)}


class GetFinancialSummarySkill(Skill):
    """Get financial summary from Odoo"""

    def __init__(self):
        super().__init__(
            name='get_financial_summary',
            description='Get financial summary from Odoo',
            group='accounting',
            version='1.0.0',
        )
        self.parameters = []

    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute financial summary retrieval"""
        try:
            logger.info("Getting financial summary")

            result = self._get_via_odoo_mcp()

            self.log_execution(kwargs, result)
            return result

        except Exception as e:
            logger.error(f"Failed to get financial summary: {e}")
            result = {'status': 'error', 'error': str(e)}
            self.log_execution(kwargs, result)
            return result

    def _get_via_odoo_mcp(self) -> Dict[str, Any]:
        """Get via Odoo MCP server"""
        import requests
        try:
            response = requests.get(
                'http://localhost:8074/tools/get_financial_summary',
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Odoo MCP error: {e}")
            return {'status': 'error', 'error': str(e)}


class GetSalesPipelineSkill(Skill):
    """Get sales pipeline from Odoo"""

    def __init__(self):
        super().__init__(
            name='get_sales_pipeline',
            description='Get sales pipeline from Odoo',
            group='accounting',
            version='1.0.0',
        )
        self.parameters = []

    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute sales pipeline retrieval"""
        try:
            logger.info("Getting sales pipeline")

            result = self._get_via_odoo_mcp()

            self.log_execution(kwargs, result)
            return result

        except Exception as e:
            logger.error(f"Failed to get sales pipeline: {e}")
            result = {'status': 'error', 'error': str(e)}
            self.log_execution(kwargs, result)
            return result

    def _get_via_odoo_mcp(self) -> Dict[str, Any]:
        """Get via Odoo MCP server"""
        import requests
        try:
            response = requests.get(
                'http://localhost:8074/tools/get_sales_pipeline',
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Odoo MCP error: {e}")
            return {'status': 'error', 'error': str(e)}
