"""
Flask configuration
"""
import os


class Config:
    """
    Configuration class
    """
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SITE_NAME = os.environ.get('SITE_NAME')