from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
import logging

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    try:
        from config import config
        app.config.from_object(config[config_name])
    except ImportError:
        # Fallback to environment variables if config.py doesn't exist
        app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///research_ai.db')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
        app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'uploads')
        app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', '')
        app.config['DEBUG'] = True
    
    # Ensure SQLALCHEMY_DATABASE_URI is set
    if 'SQLALCHEMY_DATABASE_URI' not in app.config:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///research_ai.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, app.config.get('LOG_LEVEL', 'INFO')),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Fix Flask-Login user_loader issue
    @login_manager.user_loader
    def load_user(user_id):
        # For now, return None since we don't have user authentication
        return None
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.paper_analysis import paper_analysis_bp
    from app.routes.citations import citations_bp
    from app.routes.search import search_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(paper_analysis_bp, url_prefix='/paper-analysis')
    app.register_blueprint(citations_bp, url_prefix='/citations')
    app.register_blueprint(search_bp, url_prefix='/search')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Log successful app creation
    app.logger.info(f"Research AI Flask app created with config: {config_name}")
    
    return app 