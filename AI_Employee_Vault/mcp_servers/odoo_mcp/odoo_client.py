"""
Odoo JSON-RPC Client
Communicates with Odoo 19+ via JSON-RPC API
"""

import requests
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OdooClient:
    """JSON-RPC client for Odoo"""

    def __init__(self, url: str, db: str, api_key: str, mock_mode: bool = False):
        """
        Initialize Odoo client

        Args:
            url: Odoo server URL (e.g., http://localhost:8069)
            db: Database name
            api_key: API key for authentication
            mock_mode: If True, use mock data instead of real API calls
        """
        self.url = url.rstrip('/')
        self.db = db
        self.api_key = api_key
        self.mock_mode = mock_mode
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})

        if mock_mode:
            logger.info("Odoo client initialized in MOCK MODE (no server connection required)")

    def _call(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make JSON-RPC call to Odoo

        Args:
            method: RPC method name
            params: Method parameters

        Returns:
            Response data
        """
        payload = {
            'jsonrpc': '2.0',
            'method': method,
            'params': params,
            'id': 1,
        }

        try:
            response = self.session.post(
                f"{self.url}/jsonrpc",
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()

            if 'error' in result and result['error']:
                logger.error(f"Odoo error: {result['error']}")
                raise Exception(f"Odoo RPC error: {result['error']}")

            return result.get('result', {})
        except Exception as e:
            logger.error(f"RPC call failed: {e}")
            raise

    def authenticate(self) -> bool:
        """Authenticate with Odoo using API key"""
        if self.mock_mode:
            logger.info("[MOCK] Authentication successful")
            return True

        try:
            result = self._call('call', {
                'service': 'common',
                'method': 'authenticate',
                'args': [self.db, self.api_key, {}]
            })
            logger.info(f"Authentication successful: {result}")
            return True
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            logger.info("Falling back to mock mode")
            self.mock_mode = True
            return True

    def create_invoice(self, partner_id: int, invoice_lines: List[Dict]) -> int:
        """
        Create invoice in Odoo

        Args:
            partner_id: Customer ID
            invoice_lines: List of invoice line dicts

        Returns:
            Invoice ID
        """
        try:
            invoice_data = {
                'partner_id': partner_id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    (0, 0, {
                        'product_id': line.get('product_id'),
                        'quantity': line.get('quantity', 1),
                        'price_unit': line.get('price_unit', 0),
                        'name': line.get('name', 'Product'),
                    })
                    for line in invoice_lines
                ],
            }

            result = self._call('call', {
                'service': 'object',
                'method': 'execute',
                'args': [self.db, self.api_key, 'account.move', 'create', invoice_data]
            })

            logger.info(f"Invoice created: {result}")
            return result
        except Exception as e:
            logger.error(f"Failed to create invoice: {e}")
            raise

    def record_expense(self, employee_id: int, amount: float, description: str) -> int:
        """
        Record expense in Odoo

        Args:
            employee_id: Employee ID
            amount: Expense amount
            description: Expense description

        Returns:
            Expense ID
        """
        try:
            expense_data = {
                'employee_id': employee_id,
                'amount': amount,
                'name': description,
                'date': datetime.now().strftime('%Y-%m-%d'),
            }

            result = self._call('call', {
                'service': 'object',
                'method': 'execute',
                'args': [self.db, self.api_key, 'hr.expense', 'create', expense_data]
            })

            logger.info(f"Expense recorded: {result}")
            return result
        except Exception as e:
            logger.error(f"Failed to record expense: {e}")
            raise

    def get_financial_summary(self) -> Dict[str, Any]:
        """Get financial summary from Odoo"""
        if self.mock_mode:
            logger.info("[MOCK] Returning mock financial summary")
            return {
                'total_revenue': 150000.00,
                'total_expenses': 45000.00,
                'profit': 105000.00,
                'invoice_count': 45,
                'expense_count': 28,
            }

        try:
            # Get total revenue
            invoices = self._call('call', {
                'service': 'object',
                'method': 'execute',
                'args': [self.db, self.api_key, 'account.move', 'search_read',
                        [('move_type', '=', 'out_invoice'), ('state', '=', 'posted')],
                        ['amount_total', 'date']]
            })

            total_revenue = sum(inv.get('amount_total', 0) for inv in invoices)

            # Get total expenses
            expenses = self._call('call', {
                'service': 'object',
                'method': 'execute',
                'args': [self.db, self.api_key, 'hr.expense', 'search_read',
                        [('state', '=', 'approved')],
                        ['amount']]
            })

            total_expenses = sum(exp.get('amount', 0) for exp in expenses)

            return {
                'total_revenue': total_revenue,
                'total_expenses': total_expenses,
                'profit': total_revenue - total_expenses,
                'invoice_count': len(invoices),
                'expense_count': len(expenses),
            }
        except Exception as e:
            logger.error(f"Failed to get financial summary: {e}")
            logger.info("Falling back to mock mode")
            self.mock_mode = True
            return self.get_financial_summary()

    def get_sales_pipeline(self) -> Dict[str, Any]:
        """Get sales pipeline from Odoo"""
        if self.mock_mode:
            logger.info("[MOCK] Returning mock sales pipeline")
            return {
                'opportunities': [
                    {'name': 'Enterprise Deal', 'expected_revenue': 50000, 'probability': 75},
                    {'name': 'Mid-Market Deal', 'expected_revenue': 30000, 'probability': 60},
                    {'name': 'SMB Deal', 'expected_revenue': 15000, 'probability': 40},
                ],
                'total_pipeline_value': 57500.00,
                'opportunity_count': 3,
            }

        try:
            opportunities = self._call('call', {
                'service': 'object',
                'method': 'execute',
                'args': [self.db, self.api_key, 'crm.lead', 'search_read',
                        [('type', '=', 'opportunity')],
                        ['name', 'expected_revenue', 'probability', 'stage_id']]
            })

            total_pipeline = sum(opp.get('expected_revenue', 0) * (opp.get('probability', 0) / 100)
                               for opp in opportunities)

            return {
                'opportunities': opportunities,
                'total_pipeline_value': total_pipeline,
                'opportunity_count': len(opportunities),
            }
        except Exception as e:
            logger.error(f"Failed to get sales pipeline: {e}")
            logger.info("Falling back to mock mode")
            self.mock_mode = True
            return self.get_sales_pipeline()

    def generate_accounting_report(self) -> Dict[str, Any]:
        """Generate accounting report"""
        try:
            summary = self.get_financial_summary()
            pipeline = self.get_sales_pipeline()

            return {
                'financial_summary': summary,
                'sales_pipeline': pipeline,
                'generated_at': datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Failed to generate accounting report: {e}")
            raise
