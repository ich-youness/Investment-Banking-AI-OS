#!/usr/bin/env python3
"""
Setup script for OCR client integration
This script helps you configure the OCR client for the Banking Investment OS
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

def setup_ocr_client():
    """Setup the OCR client configuration"""
    print("🔧 OCR Client Setup for Banking Investment OS")
    print("=" * 60)
    
    print("To integrate your OCR client, you need to:")
    print()
    print("1. Install your OCR client library:")
    print("   pip install your-ocr-client-library")
    print()
    print("2. Set up your API key:")
    print("   Set OCR_API_KEY environment variable")
    print("   Windows: set OCR_API_KEY=your_api_key_here")
    print("   Linux/Mac: export OCR_API_KEY=your_api_key_here")
    print()
    print("3. Update the initialize_ocr_client() function in server.py:")
    print("   Replace the placeholder code with your actual client setup")
    print()
    print("4. Example implementation:")
    print("""
def initialize_ocr_client():
    try:
        from your_ocr_client import Client
        client = Client(api_key=os.getenv("OCR_API_KEY"))
        client_ocr.set_client(client)
        api_logger.info("OCR client initialized successfully")
        return True
    except Exception as e:
        api_logger.error(f"Failed to initialize OCR client: {e}")
        return False
    """)
    print()
    print("5. Test the setup:")
    print("   python test_ocr_integration.py")
    print()
    
    # Check if OCR_API_KEY is set
    ocr_key = os.getenv("OCR_API_KEY")
    if ocr_key:
        print(f"✅ OCR_API_KEY is set: {ocr_key[:10]}...")
    else:
        print("❌ OCR_API_KEY not found in environment variables")
        print("   Please set your OCR API key")
    
    print()
    print("📝 Current OCR client status:")
    print("   - OCR module: ✅ Created (Modules/ClientOCR.py)")
    print("   - Server integration: ✅ Ready")
    print("   - Client configuration: ⚠️  Needs setup")
    print()
    print("🚀 Once configured, PDF uploads will automatically process with OCR!")

def test_ocr_integration():
    """Test the OCR integration"""
    print("🧪 Testing OCR Integration")
    print("=" * 40)
    
    try:
        from Modules.ClientOCR import client_ocr
        print("✅ OCR module imported successfully")
        
        # Check if client is set
        if client_ocr.client:
            print("✅ OCR client is configured")
        else:
            print("❌ OCR client not configured")
            print("   Please run setup_ocr_client() first")
            
    except ImportError as e:
        print(f"❌ Failed to import OCR module: {e}")
    except Exception as e:
        print(f"❌ Error testing OCR integration: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_ocr_integration()
    else:
        setup_ocr_client()
