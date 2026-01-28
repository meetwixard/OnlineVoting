import os
from dotenv import load_dotenv

# Load variables from a .env file if it exists
load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Standard SQLite for local; easily swappable for PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///secure_vote.db'

class DevelopmentConfig(Config):
    """Development-specific config."""
    DEBUG = True
    ENV = 'development'

class ProductionConfig(Config):
    """Production-specific config."""
    DEBUG = False
    ENV = 'production'
    # In production, you'd strictly enforce SSL and a real DB
    # SQLALCHEMY_DATABASE_URI = "postgresql://user:password@localhost/dbname"

# Dictionary to easily switch environments
config_setup = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
