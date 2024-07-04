"""
Review related functionality
"""

from src.models.base import Base
from src import db

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.String(36), primary_key=True)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    text = db.Column(db.String(1024), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    def __init__(self, text, user_id, place_id, created_at, updated_at, ):
        """
        New review
        """
        self.text = text
        self.user_id = user_id
        self.place_id = place_id
        self.created_at = created_at
        self.updated_at = updated_at
        
    @staticmethod
    def create(data):
        return Review(id=data['id'], place_id=data['place_id'], user_id=data['user_id'], text=data['text'])

    @staticmethod
    def update(review, data):
        review.text = data.get('text', review.text)
        return review
