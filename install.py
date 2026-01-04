"""
Quick Installation and Setup Guide
Run this to install everything needed for Fiscal-Sentinel
"""

import subprocess
import sys

def install_package(package):
    """Install a package using pip"""
    print(f"Installing {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():
    print("=" * 70)
    print("FISCAL-SENTINEL - DEPENDENCY INSTALLER")
    print("=" * 70)
    print()
    
    # Core packages first
    core_packages = [
        "fastapi==0.95.2",
        "uvicorn[standard]==0.22.0",
        "python-multipart==0.0.6",
        "numpy==1.26.4",
        "pandas==2.2.2",
        "pillow==10.1.0",
        "requests==2.31.0",
        "streamlit==1.28.0",
    ]
    
    print("Installing core packages...")
    for pkg in core_packages:
        try:
            install_package(pkg)
        except Exception as e:
            print(f"Warning: Failed to install {pkg}: {e}")
    
    # Data science packages
    ds_packages = [
        "scikit-learn==1.3.2",
        "networkx==3.2",
        "rapidfuzz==2.15.1",
        "beautifulsoup4==4.12.2",
    ]
    
    print("\nInstalling data science packages...")
    for pkg in ds_packages:
        try:
            install_package(pkg)
        except Exception as e:
            print(f"Warning: Failed to install {pkg}: {e}")
    
    # PDF and OCR
    print("\nInstalling PDF and OCR packages...")
    try:
        install_package("pdfplumber==0.7.6")
    except Exception as e:
        print(f"Warning: pdfplumber failed: {e}")
    
    try:
        install_package("pytesseract==0.3.10")
    except Exception as e:
        print(f"Warning: pytesseract failed: {e}")
        print("Note: You also need to install Tesseract OCR separately:")
        print("https://github.com/UB-Mannheim/tesseract/wiki")
    
    # PyTorch (CPU version)
    print("\nInstalling PyTorch (this may take a while)...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "torch==2.2.0",
            "--index-url", "https://download.pytorch.org/whl/cpu"
        ])
    except Exception as e:
        print(f"Warning: PyTorch installation failed: {e}")
    
    # Transformers
    print("\nInstalling Transformers...")
    try:
        install_package("transformers==4.35.0")
    except Exception as e:
        print(f"Warning: transformers failed: {e}")
    
    # spaCy
    print("\nInstalling spaCy...")
    try:
        install_package("spacy==3.6.0")
        print("Downloading spaCy language model...")
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    except Exception as e:
        print(f"Warning: spaCy installation failed: {e}")
    
    # Neo4j (optional)
    print("\nInstalling Neo4j driver (optional)...")
    try:
        install_package("neo4j==5.8.0")
    except Exception as e:
        print(f"Info: Neo4j driver not installed (optional): {e}")
    
    print()
    print("=" * 70)
    print("INSTALLATION COMPLETE!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. Run: python verify_project.py (to check everything)")
    print("2. Run: streamlit run streamlit_app.py (to start dashboard)")
    print()

if __name__ == "__main__":
    main()
