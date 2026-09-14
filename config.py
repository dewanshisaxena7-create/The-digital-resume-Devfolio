import os

# Base directory of the project
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Configuration settings for the Flask application and SQLite database.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-portfolio-secret-key-2026'
    
    # SQLite Database configuration: portfolio.db will be stored in the root folder
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'portfolio.db')
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
