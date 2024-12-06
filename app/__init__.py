"""
This module initializes the Flask app and the database
"""
from flask import Flask
from config import Config
from app.extensions import db


def create_app(config_class=Config):
    """
    Create the Flask app

    :param config_class: configuration class
    :return: Flask app
    """
    application = Flask(__name__)  # Create the Flask app
    application.config.from_object(config_class)  # Load the configuration file

    # Initialize Flask extensions here
    db.init_app(application)  # Initialize the database

    return application
