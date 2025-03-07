import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration that is common to all environments."""
    # Flask configuration
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-for-development-only')
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///login_app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security configuration
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 2592000  # 30 days in seconds
    
    # Security headers
    STRICT_TRANSPORT_SECURITY = os.getenv('STRICT_TRANSPORT_SECURITY', 'TRUE').upper() == 'TRUE'
    X_CONTENT_TYPE_OPTIONS = os.getenv('X_CONTENT_TYPE_OPTIONS', 'TRUE').upper() == 'TRUE'
    X_FRAME_OPTIONS = os.getenv('X_FRAME_OPTIONS', 'DENY')
    
    # CORS configuration
    ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '*')
    ALLOWED_METHODS = os.getenv('ALLOWED_METHODS', 'GET,POST,OPTIONS').split(',')
    ALLOW_CREDENTIALS = os.getenv('ALLOW_CREDENTIALS', 'TRUE').upper() == 'TRUE'
    
    # Rate limiting configuration
    DEFAULT_RATE_LIMIT_DAY = os.getenv('DEFAULT_RATE_LIMIT_DAY', '200')
    DEFAULT_RATE_LIMIT_HOUR = os.getenv('DEFAULT_RATE_LIMIT_HOUR', '50')
    LOGIN_RATE_LIMIT = os.getenv('LOGIN_RATE_LIMIT', '5/minute')
    REGISTER_RATE_LIMIT = os.getenv('REGISTER_RATE_LIMIT', '3/hour')
    PASSWORD_RESET_LIMIT = os.getenv('PASSWORD_RESET_LIMIT', '3/hour')
    
    # Password security
    MIN_PASSWORD_LENGTH = int(os.getenv('MIN_PASSWORD_LENGTH', '12'))
    PASSWORD_HASH_METHOD = os.getenv('PASSWORD_HASH_METHOD', 'pbkdf2:sha256')
    PASSWORD_HASH_ITERATIONS = int(os.getenv('PASSWORD_HASH_ITERATIONS', '150000'))
    
    # Content Security Policy
    CSP = {
        'default-src': [
            '\'self\'',
            '*',
            'data:',
        ] if os.getenv('FLASK_ENV') == 'development' else [
            '\'self\'',
            'cdn.jsdelivr.net',
            'cdn.tailwindcss.com',
            'unpkg.com',
            'fonts.googleapis.com',
            'fonts.gstatic.com',
        ],
        'script-src': [
            '\'self\'',
            '\'unsafe-inline\'',
            '\'unsafe-eval\'',
            '*',
        ] if os.getenv('FLASK_ENV') == 'development' else [
            '\'self\'',
            'cdn.jsdelivr.net',
            'cdn.tailwindcss.com',
            'unpkg.com',
            '\'unsafe-inline\'',
            '\'unsafe-eval\'',
        ],
        'style-src': [
            '\'self\'',
            '\'unsafe-inline\'',
            '*',
        ] if os.getenv('FLASK_ENV') == 'development' else [
            '\'self\'',
            'cdn.jsdelivr.net',
            'fonts.googleapis.com',
            'unpkg.com',
            '\'unsafe-inline\'',
        ],
        'img-src': [
            '\'self\'',
            'data:',
            'blob:',
            '*',
        ] if os.getenv('FLASK_ENV') == 'development' else [
            '\'self\'',
            'data:',
            'blob:',
            'cdn.jsdelivr.net',
        ],
        'font-src': [
            '\'self\'',
            '*',
            'data:',
        ] if os.getenv('FLASK_ENV') == 'development' else [
            '\'self\'',
            'cdn.jsdelivr.net',
            'fonts.gstatic.com',
            'fonts.googleapis.com',
        ],
        'connect-src': [
            '\'self\'',
            '*',
        ] if os.getenv('FLASK_ENV') == 'development' else [
            '\'self\'',
            'cdn.jsdelivr.net',
            'cdn.tailwindcss.com',
        ],
    }

class DevelopmentConfig(Config):
    """Configuration for development environment."""
    DEBUG = True
    FORCE_HTTPS = os.getenv('FORCE_HTTPS', 'FALSE').upper() == 'TRUE'
    SESSION_COOKIE_SECURE = os.getenv('SECURE_COOKIES', 'FALSE').upper() == 'TRUE'

class ProductionConfig(Config):
    """Configuration for production environment."""
    DEBUG = False
    FORCE_HTTPS = True
    SESSION_COOKIE_SECURE = True
    
    # In production, we'd typically have more restrictive settings
    def __init__(self):
        # Ensure SECRET_KEY is set in production
        if os.getenv('SECRET_KEY') == 'dev-key-for-development-only':
            raise ValueError('SECRET_KEY must be set to a secure value in production!')

# Set the configuration based on environment
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Return the appropriate configuration based on the environment."""
    flask_env = os.getenv('FLASK_ENV', 'development')
    return config.get(flask_env, config['default'])
