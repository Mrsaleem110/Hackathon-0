"""
Odoo MCP Server Tests
"""

import unittest
import json
from unittest.mock import Mock, patch, MagicMock
from odoo_client import OdooClient


class TestOdooClient(unittest.TestCase):
    """Test Odoo client"""

    def setUp(self):
        """Set up test fixtures"""
        self.client = OdooClient(
            url="http://localhost:8069",
            db="test_db",
            api_key="test_key"
        )

    @patch('odoo_client.requests.Session.post')
    def test_authenticate(self, mock_post):
        """Test authentication"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'result': {'uid': 2, 'username': 'admin'}
        }
        mock_post.return_value = mock_response

        result = self.client.authenticate()
        self.assertTrue(result)

    @patch('odoo_client.requests.Session.post')
    def test_create_invoice(self, mock_post):
        """Test invoice creation"""
        mock_response = Mock()
        mock_response.json.return_value = {'result': 123}
        mock_post.return_value = mock_response

        invoice_lines = [
            {
                'product_id': 1,
                'quantity': 2,
                'price_unit': 100,
                'name': 'Product A'
            }
        ]

        result = self.client.create_invoice(1, invoice_lines)
        self.assertEqual(result, 123)

    @patch('odoo_client.requests.Session.post')
    def test_record_expense(self, mock_post):
        """Test expense recording"""
        mock_response = Mock()
        mock_response.json.return_value = {'result': 456}
        mock_post.return_value = mock_response

        result = self.client.record_expense(1, 500.0, "Travel expense")
        self.assertEqual(result, 456)

    @patch('odoo_client.requests.Session.post')
    def test_get_financial_summary(self, mock_post):
        """Test financial summary"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'result': [
                {'amount_total': 1000, 'date': '2026-03-24'}
            ]
        }
        mock_post.return_value = mock_response

        result = self.client.get_financial_summary()
        self.assertIn('total_revenue', result)
        self.assertIn('total_expenses', result)
        self.assertIn('profit', result)

    @patch('odoo_client.requests.Session.post')
    def test_get_sales_pipeline(self, mock_post):
        """Test sales pipeline"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'result': [
                {
                    'name': 'Opportunity 1',
                    'expected_revenue': 5000,
                    'probability': 50
                }
            ]
        }
        mock_post.return_value = mock_response

        result = self.client.get_sales_pipeline()
        self.assertIn('opportunities', result)
        self.assertIn('total_pipeline_value', result)

    @patch('odoo_client.requests.Session.post')
    def test_generate_accounting_report(self, mock_post):
        """Test accounting report generation"""
        mock_response = Mock()
        mock_response.json.return_value = {'result': {}}
        mock_post.return_value = mock_response

        result = self.client.generate_accounting_report()
        self.assertIn('financial_summary', result)
        self.assertIn('sales_pipeline', result)
        self.assertIn('generated_at', result)


class TestOdooMCPServer(unittest.TestCase):
    """Test Odoo MCP Server"""

    def setUp(self):
        """Set up test fixtures"""
        from server import app
        self.app = app
        self.client = app.test_client()

    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['service'], 'odoo_mcp')

    def test_get_tools(self):
        """Test tools discovery endpoint"""
        response = self.client.get("/tools")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('tools', data)
        self.assertGreater(len(data['tools']), 0)

    def test_create_invoice_dry_run(self):
        """Test invoice creation in dry-run mode"""
        payload = {
            "partner_id": 1,
            "invoice_lines": [
                {
                    "product_id": 1,
                    "quantity": 1,
                    "price_unit": 100,
                    "name": "Product"
                }
            ],
            "dry_run": True
        }
        response = self.client.post(
            "/tools/create_invoice",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['mode'], 'dry_run')

    def test_record_expense_dry_run(self):
        """Test expense recording in dry-run mode"""
        payload = {
            "employee_id": 1,
            "amount": 500.0,
            "description": "Travel expense",
            "dry_run": True
        }
        response = self.client.post(
            "/tools/record_expense",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['mode'], 'dry_run')


if __name__ == '__main__':
    unittest.main()
