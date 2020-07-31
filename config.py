import os


class Config:
    """Set Flask configuration vars from .env file."""

    # General Config
    SECRET_KEY = 'HELLO'
    FLASK_APP = 'appdb.py'
    FLASK_ENV = os.environ.get('FLASK_ENV')
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')