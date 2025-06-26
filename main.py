from app import create_app
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app instance for gunicorn
app = create_app(os.getenv('FLASK_CONFIG', 'development'))

def main():
    """Main application entry point"""
    try:
        # Get configuration from environment
        config_name = os.getenv('FLASK_CONFIG', 'development')
        
        # Get port from environment or use default
        port = int(os.getenv('PORT', 5000))
        
        # Check if OpenAI API key is configured
        if not app.config.get('OPENAI_API_KEY'):
            logger.warning("OpenAI API key not configured. Some features may not work.")
            logger.info("Please set OPENAI_API_KEY environment variable or add it to config.py")
        
        logger.info(f"Starting Research AI Flask app on port {port}")
        logger.info(f"Configuration: {config_name}")
        
        # Run the app
        app.run(
            host='0.0.0.0',
            port=port,
            debug=app.config.get('DEBUG', True)
        )
        
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        raise

if __name__ == '__main__':
    main() 