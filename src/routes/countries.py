from flask import Blueprint, jsonify, request
from models.country import Country
from models.city import City
import pycountry
from flask_jwt_extended import jwt_required
from src.persistence.db import DBRepository

# Create Blueprint for country-related endpoints
country = Blueprint("country", __name__)
repository = DBRepository()

@country.route("/countries", methods=["POST"])
@jwt_required()
def add_country():
    """
    Add countries to the database using ISO country codes.
    """
    try:
        for country in pycountry.countries:
            new_country = Country(name=country.name, code=country.alpha_2)
            repository.save(new_country)
        return jsonify({"message": "Countries added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@country.route("/countries", methods=["GET"])
def get_countries():
    """
    Retrieve all countries from the database.
    """
    try:
        countries = repository.get_all(Country)
        country_list = [country.to_dict() for country in countries]
        return jsonify(country_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@country.route("/countries/<country_code>", methods=["GET"])
def get_country(country_code):
    """
    Retrieve details of a specific country by its ISO code.
    """
    country = pycountry.countries.get(alpha_2=country_code.upper())
    if country:
        country_details = Country(name=country.name, code=country.alpha_2).to_dict()
        return jsonify(country_details), 200
    else:
        return jsonify({"error": "Country not found"}), 404

@country.route("/countries/<country_code>/cities", methods=["POST"])
@jwt_required()
def add_city_to_country(country_code):
    """
    Add a city to a specific country.
    """
    try:
        country = repository.get(Country, country_code.upper())
        if not country:
            return jsonify({"error": "Country not found"}), 404

        data = request.get_json()
        city_name = data.get('name')
        if not city_name:
            return jsonify({"error": "City name is required"}), 400

        new_city = City(name=city_name, country_id=country.id)
        repository.save(new_city)
        return jsonify(new_city.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@country.route("/countries/<country_code>/cities", methods=["GET"])
def get_country_cities(country_code):
    """
    Retrieve all cities belonging to a specific country.
    """
    try:
        country = repository.get(Country, country_code.upper())
        if country:
            cities = repository.get_all(City)
            city_list = [city.to_dict() for city in cities if city.country_id == country.id]
            if city_list:
                return jsonify(city_list), 200
            else:
                return jsonify({"error": "Cities not found"}), 404
        else:
            return jsonify({"error": "Country not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
