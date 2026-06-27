import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///./test_automation_platform.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Use local storage folders in development
    BASE_STORAGE = os.getenv('BASE_STORAGE', './storage')
    UPLOAD_FOLDER = os.path.join(BASE_STORAGE, 'uploads')
    EVIDENCIAS_FOLDER = os.path.join(BASE_STORAGE, 'evidencias')
    LOGS_FOLDER = os.path.join(BASE_STORAGE, 'logs')
    
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    RPA_API_URL = os.getenv('RPA_API_URL', 'http://localhost:8000/execute')
