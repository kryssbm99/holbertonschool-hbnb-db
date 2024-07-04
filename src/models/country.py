"""
Country related functionality
"""

from src import db
from src.models.base import Base

class Country(db.Model):
    __tablename__ = 'countries'

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
        return Country(id=data['id'], name=data['name'])

    @staticmethod
    def update(country, data):
        country.name = data.get('name', country.name)
        return country
