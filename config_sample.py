# Sample Configuration file for Research AI Flask App
# Copy this file to config.py and replace with your actual API keys

import os

class Config:
    # OpenAI API Key for AI services (Required)
    # Get from: https://platform.openai.com/api-keys
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', "sk-proj-your-openai-api-key-here")
    
    # ArXiv API Key (Optional, for enhanced arXiv access)
    # Get from: https://arxiv.org/help/api
    ARXIV_API_KEY = os.environ.get('ARXIV_API_KEY', "your-arxiv-api-key-here")
    
    # Semantic Scholar API Key (Optional, for enhanced paper search)
    # Get from: https://www.semanticscholar.org/product/api
    SEMANTIC_SCHOLAR_API_KEY = os.environ.get('SEMANTIC_SCHOLAR_API_KEY', "your-semantic-scholar-api-key-here")
    
    # Flask Secret Key (Required)
    # Generate a random string for production use
    FLASK_SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', "your-secret-key-here")
    
    # Database URL (SQLite by default)
    DATABASE_URL = os.environ.get('DATABASE_URL', "sqlite:///research_ai.db")
    
    # Upload folder configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'static', 'uploads')
    
    # Model configurations
    SCIBERT_MODEL_NAME = "allenai/scibert_scivocab_uncased"
    SUMMARIZATION_MODEL = "facebook/bart-large-cnn"
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Search configurations
    DEFAULT_SEARCH_CATEGORY = "cs.LG"
    DEFAULT_MAX_RESULTS = 5
    MAX_SEARCH_RESULTS = 20
    
    # AI configurations
    OPENAI_MODEL = "gpt-3.5-turbo"
    MAX_TOKENS = 2000
    TEMPERATURE = 0.3
    
    # PDF processing configurations
    CHUNK_SIZE = 5000
    CHUNK_OVERLAP = 500
    MAX_TEXT_LENGTH = 8000
    
    # Logging configuration
    LOG_LEVEL = "INFO"
    
    # Development settings
    DEBUG = True
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    TESTING = True
    DEBUG = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 