from flask import Blueprint, jsonify, request
from models.city import City
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request
from src.persistence.db import DBRepository

# Create Blueprint for city-related endpoints
cities = Blueprint("cities", __name__)
repository = DBRepository()

@cities.route("/cities", methods=["POST", "GET"])
@jwt_required()
def manage_cities():
    """
    Create and list cities in the database.
    """
    if request.method == "POST":
        # Verify JWT
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({"msg": "Missing Authorization Header"}), 401

        # Check admin rights
        claims = get_jwt()
        if claims.get('is_admin') is not True:
            return jsonify({"msg": "Administration rights required"}), 403

        city_data = request.get_json()
        if not city_data:
            return jsonify({"Error": "Problem during city creation."}), 400

        name = city_data.get("name")
        country_id = city_data.get("country_id")

        if not name:
            return jsonify({"Error": "Missing required field."}), 400

        # Check if city already exists
        existing_city = repository.get_all(City)
        if any(city.name == name for city in existing_city):
            return jsonify({"Error": "City already exists"}), 409

        new_city = City(name=name, country_id=country_id)
        try:
            repository.save(new_city)
            return jsonify({"Success": "City added", "city": new_city.to_dict()}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    elif request.method == "GET":
        # Retrieve all cities
        try:
            cities = repository.get_all(City)
            city_list = [{
                "id": city.id,
                "name": city.name,
                "country_id": city.country_id
            } for city in cities]
            return jsonify(city_list), 200
        except Exception as e:
            return jsonify({"Error": str(e)}), 500

@cities.route("/cities/<int:city_id>", methods=["GET", "DELETE", "PUT"])
@jwt_required()
def handle_city(city_id):
    """
    Retrieve, update, or delete a specific city by its ID.
    """
    city = repository.get(City, city_id)

    if request.method == "GET":
        if city:
            return jsonify({
                "id": city.id,
                "name": city.name,
                "country_id": city.country_id
            }), 200
        return jsonify({"Error": "City not found"}), 404

    elif request.method == "PUT":
        # Verify JWT
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({"msg": "Missing Authorization Header"}), 401

        # Check admin rights
        claims = get_jwt()
        if claims.get('is_admin') is not True:
            return jsonify({"msg": "Administration rights required"}), 403

        city_data = request.get_json()
        if not city_data:
            return jsonify({"Error": "Problem during city update."}), 400

        name = city_data.get("name")
        country_id = city_data.get("country_id")

        if not name:
            return jsonify({"Error": "Missing required field."}), 400

        if not city:
            return jsonify({"Error": "City not found"}), 404

        city.name = name
        city.country_id = country_id
        try:
            repository.update(city)
            return jsonify({"Success": "City updated"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    elif request.method == "DELETE":
        # Verify JWT and check admin rights
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({"msg": "Missing Authorization Header"}), 401

        claims = get_jwt()
        if claims.get('is_admin') is not True:
            return jsonify({"msg": "Administration rights required"}), 403

        if not city:
            return jsonify({"Error": "City not found"}), 404
        try:
            repository.delete(city)
            return jsonify({"Success": "City deleted"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
