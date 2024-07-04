"""
  Now is easy to implement the database repository. The DBRepository
  should implement the Repository (Storage) interface and the methods defined
  in the abstract class Storage.

  The methods to implement are:
    - get_all
    - get
    - save
    - update
    - delete
    - reload (which can be empty)
"""

from src import db
from src.persistence.repository import Repository
from src.models.user import User
from src.models.city import City
from src.models.country import Country
from src.models.place import Place
from src.models.review import Review
from src.models.amenity import Amenity

class DBRepository(Repository):
    def __init__(self):
        self.user_model = User
        self.city_model = City
        self.country_model = Country
        self.place_model = Place
        self.review_model = Review
        self.amenity_model = Amenity

    def get(self, model, id):
        return model.query.get(id)

    def get_all(self, model):
        return model.query.all()

    def save(self, obj):
        db.session.add(obj)
        db.session.commit()

    def delete(self, obj):
        db.session.delete(obj)
        db.session.commit()

    def update(self, obj):
        db.session.commit()
        
    def reload(self) -> None:
