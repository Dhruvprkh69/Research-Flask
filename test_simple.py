import os
import sys

print("Testing basic imports...")

try:
    import app
    print("✅ app imported successfully")
except Exception as e:
    print(f"❌ app import failed: {e}")

try:
    import app.services
    print("✅ app.services imported successfully")
except Exception as e:
    print(f"❌ app.services import failed: {e}")

try:
    from app.services.ai_service import AIService
    print("✅ AIService imported successfully")
except Exception as e:
    print(f"❌ AIService import failed: {e}")

print("Test completed!") 