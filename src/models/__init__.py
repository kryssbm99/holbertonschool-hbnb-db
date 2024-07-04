"""Initializing the app  """
from flask_sqlalchemy import SQLAlchemy
from .user import User
db = SQLAlchemy()

def app_init(app):
    db.app_init(app)
    
__all__ = ['User']