from flask import Blueprint, jsonify, request
from models.place import Place
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from src.persistence.db import DBRepository

# Create Blueprint for place-related endpoints
place = Blueprint("place", __name__)
repository = DBRepository()

@place.route("/places", methods=["POST", "GET"])
def add_place():
    """
    Create and list places.
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

        place_data = request.get_json()
        if not place_data:
            return jsonify({"Error": "Problem during place creation"})

        # Extract and validate data
        name = place_data.get("name")
        description = place_data.get("description")
        city_id = place_data.get("city_id")

        if not all([name, description, city_id]):
            return jsonify({"Error": "Missing required field."}), 400

        # Check data types
        if not isinstance(name, str) or not isinstance(description, str):
            return jsonify({"Error": "Invalid data type for name or description."}), 400
        if not isinstance(city_id, int):
            return jsonify({"Error": "Invalid data type for city_id."}), 400

        # Create new place
        new_place = Place(name=name, description=description, city_id=city_id)

        try:
            repository.save(new_place)
            return jsonify({"Success": "Place added", "place": new_place.to_dict()}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    else:
        # Retrieve all places
        try:
            places = repository.get_all(Place)
            place_list = [{
                "name": place.name,
                "city_id": place.city_id,
                "description": place.description,
                "created_at": place.created_at,
                "updated_at": place.updated_at
            } for place in places]
            return jsonify(place_list), 200
        except Exception as e:
            return jsonify({"Error": "No place found"}), 404

@place.route("/places/<string:id>", methods=["GET", "DELETE", "PUT"])
def get_place(id):
    """
    Retrieve, update, or delete a specific place.
    """
    place = repository.get(Place, id)

    if request.method == "GET":
        if not place:
            return jsonify({"Error": "Place not found"}), 404
        return jsonify({
            "name": place.name,
            "city_id": place.city_id,
            "description": place.description,
            "created_at": place.created_at,
            "updated_at": place.updated_at
        }), 200

    if request.method == "DELETE":
        # Verify JWT and check admin rights
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({"msg": "Missing Authorization Header"}), 401

        claims = get_jwt()
        if claims.get('is_admin') is not True:
            return jsonify({"msg": "Administration rights required"}), 403

        if not place:
            return jsonify({"Error": "Place not found"}), 404

        repository.delete(place)
        return jsonify({"Success": "Place deleted"}), 200

    if request.method == "PUT":
        # Verify JWT and check admin rights
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({"msg": "Missing Authorization Header"}), 401

        claims = get_jwt()
        if claims.get('is_admin') is not True:
            return jsonify({"msg": "Administration rights required"}), 403

        if not place:
            return jsonify({"Error": "Place not found"}), 404

        # Update place data
        place_data = request.get_json()
        place.name = place_data.get("name", place.name)
        place.description = place_data.get("description", place.description)
        place.city_id = place_data.get("city_id", place.city_id)
        repository.update(place)
        return jsonify({"Success": "Place updated"}), 200
