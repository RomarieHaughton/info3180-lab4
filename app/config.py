import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    """Base Config Object"""
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'Som3$ec5etK*y')  
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', './uploads')  
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', '').replace('postgres://', 'postgresql://')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  
