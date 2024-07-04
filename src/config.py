"""
This module exports configuration classes for the Flask application.

- DevelopmentConfig
- TestingConfig
- ProductionConfig

"""
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///hbnb.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hbnb.db'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hbnb_test.db'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///hbnb.db'

def get_config(config_class):
    if config_class == 'development':
        return DevelopmentConfig
    elif config_class == 'testing':
        return TestingConfig
    elif config_class == 'production':
        return ProductionConfig
    else:
        return Config
