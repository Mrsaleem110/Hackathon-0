"""
Odoo MCP Server
FastAPI server exposing Odoo accounting operations as MCP tools
Port: 8074
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

from .odoo_client import OdooClient

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Odoo MCP Server", version="1.0.0")

# Initialize Odoo client
ODOO_URL = os.getenv('ODOO_URL', 'http://localhost:8069')
ODOO_DB = os.getenv('ODOO_DB', 'odoo_vault')
ODOO_API_KEY = os.getenv('ODOO_API_KEY', '')

odoo_client = None

# Request/Response models
class CreateInvoiceRequest(BaseModel):
    partner_id: int
    invoice_lines: list
    dry_run: bool = False

class RecordExpenseRequest(BaseModel):
    employee_id: int
    amount: float
    description: str
    dry_run: bool = False

class ApprovalRequest(BaseModel):
    action: str
    parameters: Dict[str, Any]
    reviewer: str = "system"
    notes: str = ""

# Initialize Odoo client on startup
@app.on_event("startup")
async def startup_event():
    global odoo_client
    try:
        odoo_client = OdooClient(ODOO_URL, ODOO_DB, ODOO_API_KEY)
        if odoo_client.authenticate():
            logger.info("Odoo client initialized and authenticated")
        else:
            logger.warning("Odoo authentication failed")
    except Exception as e:
        logger.error(f"Failed to initialize Odoo client: {e}")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "odoo_mcp",
        "timestamp": datetime.now().isoformat(),
        "odoo_url": ODOO_URL,
        "odoo_db": ODOO_DB,
    }

# MCP tools discovery endpoint
@app.get("/tools")
async def get_tools():
    """Get available MCP tools"""
    return {
        "tools": [
            {
                "name": "create_invoice",
                "description": "Create invoice in Odoo",
                "parameters": {
                    "partner_id": "Customer ID",
                    "invoice_lines": "List of invoice lines",
                    "dry_run": "Test mode (default: false)",
                }
            },
            {
                "name": "record_expense",
                "description": "Record expense in Odoo",
                "parameters": {
                    "employee_id": "Employee ID",
                    "amount": "Expense amount",
                    "description": "Expense description",
                    "dry_run": "Test mode (default: false)",
                }
            },
            {
                "name": "get_financial_summary",
                "description": "Get financial summary from Odoo",
                "parameters": {}
            },
            {
                "name": "get_sales_pipeline",
                "description": "Get sales pipeline from Odoo",
                "parameters": {}
            },
            {
                "name": "generate_accounting_report",
                "description": "Generate accounting report",
                "parameters": {}
            },
        ]
    }

# Tool endpoints
@app.post("/tools/create_invoice")
async def create_invoice(request: CreateInvoiceRequest):
    """Create invoice in Odoo"""
    try:
        if request.dry_run:
            logger.info(f"DRY RUN: Would create invoice for partner {request.partner_id}")
            return {
                "status": "success",
                "mode": "dry_run",
                "message": f"Would create invoice for partner {request.partner_id}",
                "invoice_id": None,
            }

        # Check if approval needed
        if len(request.invoice_lines) > 0:
            total_amount = sum(line.get('price_unit', 0) * line.get('quantity', 1)
                             for line in request.invoice_lines)
            if total_amount > 10000:  # Approval threshold
                return {
                    "status": "pending_approval",
                    "message": "Invoice requires approval (amount > 10000)",
                    "approval_request": {
                        "action": "create_invoice",
                        "parameters": request.dict(),
                        "timestamp": datetime.now().isoformat(),
                    }
                }

        # Create invoice
        invoice_id = odoo_client.create_invoice(
            request.partner_id,
            request.invoice_lines
        )

        # Log action
        log_action("create_invoice", {
            "partner_id": request.partner_id,
            "invoice_id": invoice_id,
            "line_count": len(request.invoice_lines),
        })

        return {
            "status": "success",
            "invoice_id": invoice_id,
            "message": f"Invoice {invoice_id} created successfully",
        }
    except Exception as e:
        logger.error(f"Failed to create invoice: {e}")
        return {
            "status": "error",
            "error": str(e),
        }

@app.post("/tools/record_expense")
async def record_expense(request: RecordExpenseRequest):
    """Record expense in Odoo"""
    try:
        if request.dry_run:
            logger.info(f"DRY RUN: Would record expense of {request.amount}")
            return {
                "status": "success",
                "mode": "dry_run",
                "message": f"Would record expense of {request.amount}",
                "expense_id": None,
            }

        # Check if approval needed
        if request.amount > 5000:  # Approval threshold
            return {
                "status": "pending_approval",
                "message": "Expense requires approval (amount > 5000)",
                "approval_request": {
                    "action": "record_expense",
                    "parameters": request.dict(),
                    "timestamp": datetime.now().isoformat(),
                }
            }

        # Record expense
        expense_id = odoo_client.record_expense(
            request.employee_id,
            request.amount,
            request.description
        )

        # Log action
        log_action("record_expense", {
            "employee_id": request.employee_id,
            "expense_id": expense_id,
            "amount": request.amount,
        })

        return {
            "status": "success",
            "expense_id": expense_id,
            "message": f"Expense {expense_id} recorded successfully",
        }
    except Exception as e:
        logger.error(f"Failed to record expense: {e}")
        return {
            "status": "error",
            "error": str(e),
        }

@app.get("/tools/get_financial_summary")
async def get_financial_summary():
    """Get financial summary"""
    try:
        summary = odoo_client.get_financial_summary()
        log_action("get_financial_summary", summary)
        return {
            "status": "success",
            "data": summary,
        }
    except Exception as e:
        logger.error(f"Failed to get financial summary: {e}")
        return {
            "status": "error",
            "error": str(e),
        }

@app.get("/tools/get_sales_pipeline")
async def get_sales_pipeline():
    """Get sales pipeline"""
    try:
        pipeline = odoo_client.get_sales_pipeline()
        log_action("get_sales_pipeline", {"opportunity_count": pipeline.get("opportunity_count")})
        return {
            "status": "success",
            "data": pipeline,
        }
    except Exception as e:
        logger.error(f"Failed to get sales pipeline: {e}")
        return {
            "status": "error",
            "error": str(e),
        }

@app.get("/tools/generate_accounting_report")
async def generate_accounting_report():
    """Generate accounting report"""
    try:
        report = odoo_client.generate_accounting_report()
        log_action("generate_accounting_report", {"generated_at": report.get("generated_at")})
        return {
            "status": "success",
            "data": report,
        }
    except Exception as e:
        logger.error(f"Failed to generate accounting report: {e}")
        return {
            "status": "error",
            "error": str(e),
        }

def log_action(action_type: str, parameters: Dict[str, Any]):
    """Log action to audit trail"""
    try:
        logs_dir = Path(__file__).parent.parent.parent / "Logs"
        logs_dir.mkdir(exist_ok=True)

        log_file = logs_dir / f"{datetime.now().strftime('%Y-%m-%d')}.json"

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "service": "odoo_mcp",
            "action_type": action_type,
            "parameters": parameters,
        }

        # Append to log file
        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = json.load(f)
        else:
            logs = []

        logs.append(log_entry)

        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)

        logger.info(f"Action logged: {action_type}")
    except Exception as e:
        logger.error(f"Failed to log action: {e}")

if __name__ == "__main__":
    port = int(os.getenv('ODOO_MCP_PORT', 8074))
    uvicorn.run(app, host="0.0.0.0", port=port)
