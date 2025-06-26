from app import create_app
import os

# Create Flask app instance for gunicorn
app = create_app(os.getenv('FLASK_CONFIG', 'production')) 