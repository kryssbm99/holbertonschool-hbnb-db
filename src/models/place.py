"""
Place related functionality
"""

from src.models.base import Base
from src import db

class Place(db.Model):
    __tablename__ = 'places'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    city_id = db.Column(db.String(36), db.ForeignKey('cities.id'), nullable=False)
    description = db.Column(db.String(512))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'city_id': self.city_id,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    @staticmethod
    def create(data):
        return Place(id=data['id'], name=data['name'], city_id=data['city_id'], description=data.get('description'))

    @staticmethod
    def update(place, data):
        place.name = data.get('name', place.name)
        place.city_id = data.get('city_id', place.city_id)
        place.description = data.get('description', place.description)
        return place
