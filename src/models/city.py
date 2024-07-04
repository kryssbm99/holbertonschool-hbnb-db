"""
City related functionality
"""

from src.models.base import Base
from src import db

class City(db.Model):
    __tablename__ = 'cities'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    country_id = db.Column(db.String(36), db.ForeignKey('countries.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'country_id': self.country_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    @staticmethod
    def create(data):
        return City(id=data['id'], name=data['name'], country_id=data['country_id'])

    @staticmethod
    def update(city, data):
        city.name = data.get('name', city.name)
        city.country_id = data.get('country_id', city.country_id)
        return city
