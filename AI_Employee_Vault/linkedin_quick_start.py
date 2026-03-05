#!/usr/bin/env python3
"""
Quick Start - LinkedIn Create Post Button
One command to get everything set up
"""
import sys
from pathlib import Path
import webbrowser
import time

def print_header():
    print("\n" + "="*70)
    print("🚀 LINKEDIN CREATE POST BUTTON - QUICK START")
    print("="*70 + "\n")

def show_setup_options():
    print("Choose your setup method:\n")
    print("1️⃣  QUICK SETUP (Recommended)")
    print("   └─ Install Tampermonkey + userscript (2 minutes)")
    print("   └─ Button appears on Agentic Sphere page automatically\n")

    print("2️⃣  FULL INTEGRATION")
    print("   └─ Python integration with vault workflow")
    print("   └─ Create posts with approval workflow\n")

    print("3️⃣  OPEN AGENTIC SPHERE PAGE")
    print("   └─ Open page in browser now\n")

    print("4️⃣  VIEW DOCUMENTATION")
    print("   └─ Read setup guide\n")

    print("5️⃣  EXIT\n")

def show_quick_setup():
    print("\n" + "="*70)
    print("QUICK SETUP - TAMPERMONKEY USERSCRIPT")
    print("="*70 + "\n")

    print("Step 1: Install Tampermonkey")
    print("  • Chrome: https://chrome.google.com/webstore/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobp55f")
    print("  • Firefox: https://addons.mozilla.org/en-US/firefox/addon/tampermonkey/")
    print("  • Edge: https://microsoftedge.microsoft.com/addons/detail/tampermonkey/iikmkjmpaadaobahmlepeloendndfohd\n")

    print("Step 2: Create New Script in Tampermonkey")
    print("  • Click Tampermonkey icon → Create a new script")
    print("  • Delete default template\n")

    print("Step 3: Copy Script Content")
    print("  • Open: linkedin_create_post_button.js")
    print("  • Copy all content")
    print("  • Paste into Tampermonkey editor\n")

    print("Step 4: Save & Enable")
    print("  • Press Ctrl+S to save")
    print("  • Script is now active!\n")

    print("Step 5: Test It")
    print("  • Go to: https://www.linkedin.com/company/agentic-sphere/")
    print("  • Look for purple '✨ Create Post' button")
    print("  • Click to open post editor\n")

    input("Press Enter to open the script file...")
    script_path = Path("linkedin_create_post_button.js")
    if script_path.exists():
        print(f"✓ Script file found: {script_path}")
        print(f"  Copy the content and paste into Tampermonkey\n")
    else:
        print("⚠ Script file not found. Please check the file exists.\n")

def show_full_integration():
    print("\n" + "="*70)
    print("FULL INTEGRATION - PYTHON WORKFLOW")
    print("="*70 + "\n")

    print("This option integrates with your Agentic Sphere vault:\n")
    print("Workflow:")
    print("  1. Create post template")
    print("  2. Post moves to Needs_Action/")
    print("  3. Review and approve")
    print("  4. Move to Pending_Approval/Approved/")
    print("  5. Orchestrator publishes automatically\n")

    print("To use:")
    print("  python linkedin_button_integration.py\n")

    input("Press Enter to launch integration...")
    import subprocess
    try:
        subprocess.run([sys.executable, "linkedin_button_integration.py"])
    except Exception as e:
        print(f"Error: {e}")

def open_agentic_sphere():
    print("\n" + "="*70)
    print("OPENING AGENTIC SPHERE PAGE")
    print("="*70 + "\n")

    url = "https://www.linkedin.com/company/agentic-sphere/"
    print(f"Opening: {url}\n")

    try:
        webbrowser.open(url)
        print("✓ Page opened in your default browser")
        print("✓ Look for the purple '✨ Create Post' button")
        print("✓ If you don't see it, make sure Tampermonkey is installed\n")
        time.sleep(2)
    except Exception as e:
        print(f"Error opening browser: {e}")
        print(f"Please visit manually: {url}\n")

def show_documentation():
    print("\n" + "="*70)
    print("DOCUMENTATION")
    print("="*70 + "\n")

    docs = [
        ("LINKEDIN_CREATE_POST_GUIDE.md", "Complete guide with all features"),
        ("LINKEDIN_BUTTON_SETUP.md", "Installation instructions"),
        ("linkedin_create_post_button.js", "Tampermonkey userscript"),
        ("linkedin_button_integration.py", "Python integration script"),
    ]

    print("Available documentation:\n")
    for i, (filename, description) in enumerate(docs, 1):
        filepath = Path(filename)
        exists = "✓" if filepath.exists() else "✗"
        print(f"{exists} {i}. {filename}")
        print(f"   └─ {description}\n")

    print("Open any file to read the documentation.\n")

def main():
    print_header()

    while True:
        show_setup_options()
        choice = input("Select option (1-5): ").strip()

        if choice == "1":
            show_quick_setup()
        elif choice == "2":
            show_full_integration()
        elif choice == "3":
            open_agentic_sphere()
        elif choice == "4":
            show_documentation()
        elif choice == "5":
            print("\n✓ Goodbye!\n")
            break
        else:
            print("❌ Invalid option. Please try again.\n")

        input("\nPress Enter to continue...")
        print("\n" * 2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✓ Exited\n")
        sys.exit(0)
