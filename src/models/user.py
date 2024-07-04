"""
User related functionality
"""

from .base import Base
from src import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(Base, db.Model):
    """User representation"""
    tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())
    
    """Password Config"""
    def set_password(self, password):
        
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
       
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
    }
                
    @staticmethod
    def create(data):
        return User(id=data['id'], email=data['email'], password=data['password'], is_admin=data['is_admin'])

    @staticmethod
    def update(user, data):
        user.email = data.get('email', user.email)
        user.password = data.get('password', user.password)
        user.is_admin = data.get('is_admin', user.is_admin)
        return user
