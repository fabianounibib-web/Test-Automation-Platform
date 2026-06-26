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
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', '/app/storage/uploads')
    EVIDENCIAS_FOLDER = os.getenv('EVIDENCIAS_FOLDER', '/app/storage/evidencias')
    LOGS_FOLDER = os.getenv('LOGS_FOLDER', '/app/storage/logs')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))
    REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
    RPA_API_URL = os.getenv('RPA_API_URL', 'http://rpa:8000/execute')
