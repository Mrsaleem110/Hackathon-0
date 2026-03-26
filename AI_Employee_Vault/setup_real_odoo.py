#!/usr/bin/env python3
"""
Setup Real Odoo - Interactive guide to get Odoo 19+ running
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def print_step(num, text):
    print(f"\n[STEP {num}] {text}")
    print("-" * 70)

def check_odoo_running():
    """Check if Odoo is running on localhost:8069"""
    try:
        import requests
        response = requests.get("http://localhost:8069", timeout=2)
        return True
    except:
        return False

def main():
    print_header("ODOO 19+ SETUP FOR AI EMPLOYEE VAULT")

    # Check if already running
    if check_odoo_running():
        print("\n[OK] Odoo is already running on localhost:8069!")
        print("\nNow setting up credentials...")
        setup_credentials()
        return

    print("\n[INFO] Odoo not detected on localhost:8069")
    print("\nChoose your setup method:")
    print("\n1. Docker (Recommended - Fastest)")
    print("2. Windows Installer")
    print("3. Manual Installation")
    print("4. Use Mock Mode (No installation needed)")

    choice = input("\nEnter choice (1-4): ").strip()

    if choice == "1":
        setup_docker()
    elif choice == "2":
        setup_windows()
    elif choice == "3":
        setup_manual()
    elif choice == "4":
        print("\n[OK] Using mock mode - no installation needed")
        print("Odoo will work with realistic test data")
    else:
        print("Invalid choice")
        sys.exit(1)

def setup_docker():
    """Setup Odoo using Docker"""
    print_step(1, "Install Docker Desktop")
    print("""
    1. Download Docker Desktop from: https://www.docker.com/products/docker-desktop
    2. Install and restart your computer
    3. Come back and run this script again
    """)

    print_step(2, "Run Odoo in Docker")
    print("""
    Once Docker is installed, run this command in PowerShell:

    docker run -d -p 8069:8069 --name odoo19 ^
      -e POSTGRES_PASSWORD=odoo ^
      -e POSTGRES_USER=odoo ^
      -e POSTGRES_DB=odoo ^
      odoo:19

    This will:
    - Download Odoo 19 image
    - Start PostgreSQL database
    - Start Odoo on localhost:8069
    - Take 2-3 minutes first time
    """)

    print_step(3, "Access Odoo")
    print("""
    Once running:
    1. Open: http://localhost:8069
    2. Create admin account
    3. Create a database
    4. Get API key from Settings > Users > Your User
    """)

    print_step(4, "Configure AI Employee Vault")
    setup_credentials()

def setup_windows():
    """Setup Odoo on Windows"""
    print_step(1, "Download Odoo Installer")
    print("""
    1. Go to: https://www.odoo.com/en_US/download
    2. Download Odoo 19 for Windows
    3. Run the installer
    4. Choose default settings
    5. PostgreSQL will be installed automatically
    """)

    print_step(2, "Start Odoo")
    print("""
    After installation:
    1. Odoo should start automatically
    2. Open: http://localhost:8069
    3. Create admin account
    4. Create a database
    """)

    print_step(3, "Get API Key")
    print("""
    1. Login to Odoo
    2. Go to Settings > Users
    3. Click on your user
    4. Scroll to API Keys section
    5. Generate new API key
    6. Copy the key
    """)

    print_step(4, "Configure AI Employee Vault")
    setup_credentials()

def setup_manual():
    """Setup Odoo manually"""
    print_step(1, "Install Python 3.10+")
    print("""
    Download from: https://www.python.org/downloads/
    Make sure to check "Add Python to PATH"
    """)

    print_step(2, "Install PostgreSQL")
    print("""
    Download from: https://www.postgresql.org/download/windows/
    Remember the password you set for postgres user
    """)

    print_step(3, "Clone Odoo Repository")
    print("""
    Open Command Prompt and run:

    git clone https://github.com/odoo/odoo.git --depth 1 --branch 19.0
    cd odoo
    """)

    print_step(4, "Install Dependencies")
    print("""
    pip install -r requirements.txt
    pip install psycopg2-binary
    """)

    print_step(5, "Create Odoo Config")
    print("""
    Create file: odoo.conf

    [options]
    addons_path = addons
    admin_passwd = admin
    db_host = localhost
    db_port = 5432
    db_user = postgres
    db_password = YOUR_POSTGRES_PASSWORD
    db_name = odoo
    http_port = 8069
    """)

    print_step(6, "Start Odoo")
    print("""
    python odoo-bin -c odoo.conf

    Then open: http://localhost:8069
    """)

    print_step(7, "Configure AI Employee Vault")
    setup_credentials()

def setup_credentials():
    """Setup Odoo credentials in .env"""
    print_step(1, "Verify Odoo is Running")

    if not check_odoo_running():
        print("[ERROR] Odoo not detected on localhost:8069")
        print("Please start Odoo first, then run this script again")
        sys.exit(1)

    print("[OK] Odoo detected on localhost:8069")

    print_step(2, "Get Odoo Credentials")

    url = input("\nOdoo URL [http://localhost:8069]: ").strip() or "http://localhost:8069"
    db = input("Database name [odoo]: ").strip() or "odoo"
    api_key = input("API Key (from Settings > Users > Your User): ").strip()

    if not api_key:
        print("[ERROR] API key is required")
        sys.exit(1)

    print_step(3, "Update .env File")

    env_file = Path(".env")
    if env_file.exists():
        content = env_file.read_text()
    else:
        content = ""

    # Add or update Odoo settings
    lines = content.split('\n')
    new_lines = []

    for line in lines:
        if not line.startswith('ODOO_'):
            new_lines.append(line)

    # Add Odoo config
    new_lines.append(f"\n# Odoo Configuration")
    new_lines.append(f"ODOO_URL={url}")
    new_lines.append(f"ODOO_DB={db}")
    new_lines.append(f"ODOO_API_KEY={api_key}")

    env_file.write_text('\n'.join(new_lines))

    print(f"[OK] Updated .env with:")
    print(f"   ODOO_URL={url}")
    print(f"   ODOO_DB={db}")
    print(f"   ODOO_API_KEY=***")

    print_step(4, "Test Connection")

    test_odoo(url, db, api_key)

def test_odoo(url, db, api_key):
    """Test Odoo connection"""
    try:
        from mcp_servers.odoo_mcp.odoo_client import OdooClient

        print("\nTesting Odoo connection...")
        odoo = OdooClient(url=url, db=db, api_key=api_key, mock_mode=False)

        if odoo.authenticate():
            print("[OK] Authentication successful!")

            summary = odoo.get_financial_summary()
            print(f"\nFinancial Summary:")
            print(f"   Revenue: ${summary.get('total_revenue', 0):,.2f}")
            print(f"   Expenses: ${summary.get('total_expenses', 0):,.2f}")
            print(f"   Profit: ${summary.get('profit', 0):,.2f}")

            pipeline = odoo.get_sales_pipeline()
            print(f"\nSales Pipeline:")
            print(f"   Opportunities: {pipeline.get('opportunity_count', 0)}")
            print(f"   Pipeline Value: ${pipeline.get('total_pipeline_value', 0):,.2f}")

            print("\n[SUCCESS] ODOO IS FULLY OPERATIONAL!")
            print("\nYou can now use real Odoo data in AI Employee Vault")
        else:
            print("[ERROR] Authentication failed")
            print("Check your API key and try again")

    except Exception as e:
        print(f"[ERROR] {e}")
        print("Make sure Odoo is running and credentials are correct")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled")
        sys.exit(0)
