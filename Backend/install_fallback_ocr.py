#!/usr/bin/env python3
"""
Install fallback OCR dependencies
Installs pypdf for basic PDF text extraction
"""

import subprocess
import sys

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def test_imports():
    """Test if pypdf can be imported"""
    try:
        import pypdf
        print("✅ pypdf imported successfully!")
        return True
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False

def main():
    print("🔧 Installing Fallback OCR Dependencies")
    print("=" * 50)
    print("This will install pypdf for basic PDF text extraction")
    print("This is used as a fallback when advanced OCR is not available")
    print()
    
    # Install pypdf
    package = "pypdf>=3.0.0"
    print(f"📦 Installing {package}...")
    
    if install_package(package):
        print(f"✅ Successfully installed {package}")
    else:
        print(f"❌ Failed to install {package}")
        return
    
    # Test imports
    print("\n🔍 Testing package import...")
    if test_imports():
        print("✅ Fallback OCR setup complete!")
        print("\n🚀 You can now upload PDFs and they will be processed with basic text extraction!")
        print("   - Advanced OCR: Not configured (will use fallback)")
        print("   - Fallback OCR: ✅ Ready (pypdf)")
    else:
        print("❌ Setup incomplete. Please check the error messages above.")

if __name__ == "__main__":
    main()
