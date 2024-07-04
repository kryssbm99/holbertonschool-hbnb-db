"""
Amenity related functionality
"""

from src.models.base import Base
from src import db

class Amenity(db.Model):
    __tablename__ = 'amenities'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    @staticmethod
    def create(data):
        return Amenity(id=data['id'], name=data['name'])

    @staticmethod
    def update(amenity, data):
        amenity.name = data.get('name', amenity.name)
        return amenity
