import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Path configurations
    TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'templates')
    STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
    MAX_CONTENT_LENGTH = 30 * 1024 * 1024 #size limit for uploaded files (30MB)
    
    # Flask configuration
    SECRET_KEY = 'secretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    