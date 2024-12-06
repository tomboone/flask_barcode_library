"""
Flask extensions
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager  # type: ignore


db = SQLAlchemy()  # Database

login_manager = LoginManager()  # Login manager
