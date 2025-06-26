#!/usr/bin/env python3
"""
Simple test script to check if the Flask app can be created successfully
"""

try:
    print("Testing Flask app creation...")
    from app import create_app
    
    print("✅ App factory imported successfully")
    
    app = create_app()
    print("✅ Flask app created successfully")
    
    print("✅ All tests passed! The Flask app is ready to run.")
    print("\nTo run the app:")
    print("python run.py")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all dependencies are installed: pip install -r requirements.txt")
    
except Exception as e:
    print(f"❌ Error creating app: {e}")
    print("Check the error message above for details") 