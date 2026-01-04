"""
Master script to verify complete project setup
Run this to ensure everything is ready for demo
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if Path(filepath).exists():
        print(f"  ✅ {description}")
        return True
    else:
        print(f"  ❌ MISSING: {description}")
        return False

def main():
    print("=" * 70)
    print("FISCAL-SENTINEL PROJECT VERIFICATION")
    print("=" * 70)
    
    all_checks_passed = True
    
    # Check core application files
    print("\n📦 Core Application Files:")
    files_to_check = [
        ("app/main.py", "FastAPI backend"),
        ("app/modules/tender_watch.py", "Tender-Watch module"),
        ("app/modules/price_guard.py", "Price-Guard module"),
        ("app/modules/graph_fraud.py", "Ghost-Hunter module"),
        ("app/modules/welfare_shield.py", "Welfare-Shield module"),
        ("streamlit_app.py", "Streamlit dashboard"),
        ("config.py", "Configuration file"),
        ("requirements.txt", "Dependencies list"),
    ]
    
    for filepath, desc in files_to_check:
        if not check_file_exists(filepath, desc):
            all_checks_passed = False
    
    # Check sample data files
    print("\n📊 Sample Data Files:")
    data_files = [
        ("data/samples/sample_payroll.csv", "Payroll CSV"),
        ("data/samples/sample_death_registry.csv", "Death Registry CSV"),
        ("data/samples/sample_disbursements.csv", "Disbursements CSV"),
        ("data/samples/sample_tender_1.txt", "Tender Document 1"),
        ("data/samples/sample_tender_2.txt", "Tender Document 2"),
    ]
    
    for filepath, desc in data_files:
        if not check_file_exists(filepath, desc):
            all_checks_passed = False
    
    # Check documentation
    print("\n📖 Documentation:")
    doc_files = [
        ("README.md", "Main README"),
        ("DEMO_GUIDE.md", "Demo Instructions"),
        ("CHECKLIST.md", "Project Checklist"),
    ]
    
    for filepath, desc in doc_files:
        if not check_file_exists(filepath, desc):
            all_checks_passed = False
    
    # Check utility scripts
    print("\n🛠️ Utility Scripts:")
    script_files = [
        ("setup.bat", "Setup script"),
        ("run_api.bat", "API launcher"),
        ("run_dashboard.bat", "Dashboard launcher"),
        ("test_modules.py", "Module tests"),
        ("generate_sample_data.py", "Sample data generator"),
    ]
    
    for filepath, desc in script_files:
        if not check_file_exists(filepath, desc):
            all_checks_passed = False
    
    # Check Python installation
    print("\n🐍 Python Environment:")
    try:
        python_version = sys.version
        print(f"  ✅ Python installed: {python_version.split()[0]}")
    except:
        print(f"  ❌ Python check failed")
        all_checks_passed = False
    
    # Final summary
    print("\n" + "=" * 70)
    if all_checks_passed:
        print("✅ ALL CHECKS PASSED - PROJECT IS READY!")
        print("=" * 70)
        print("\n🚀 Next Steps:")
        print("  1. Run: setup.bat          (Install dependencies)")
        print("  2. Run: run_dashboard.bat  (Start the demo)")
        print("  3. Read: DEMO_GUIDE.md     (For demo instructions)")
        print("\n💡 Tip: Run 'python generate_sample_data.py' for extended test data")
    else:
        print("⚠️  SOME CHECKS FAILED - PLEASE REVIEW ABOVE")
        print("=" * 70)
        print("\nSome files may be missing. This could be normal if:")
        print("  - You haven't run the full setup yet")
        print("  - Some files are optional (e.g., extended sample data)")
    
    print("\n" + "=" * 70)
    print("Project Directory:", os.getcwd())
    print("=" * 70)

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")
