from flask import Blueprint, jsonify, request
from models.amenity import Amenity
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request
from src.persistence.db import DBRepository

# Create Blueprint for amenity-related endpoints
amenities = Blueprint("amenities", __name__)
repository = DBRepository()

@amenities.route("/amenities", methods=["POST", 'GET'])
@jwt_required()
def manage_amenities():
    """
    Create and list amenities in the database.
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

        amenity_data = request.get_json()
        if not amenity_data:
            return jsonify({"Error": "Problem during amenity creation."}), 400

        name = amenity_data.get("name")

        if not name:
            return jsonify({"Error": "Missing required field."}), 400

        # Check if amenity already exists
        existing_amenity = repository.get_all(Amenity)
        if any(amenity.name == name for amenity in existing_amenity):
            return jsonify({"Error": "Amenity already exists"}), 409

        new_amenity = Amenity(name=name)
        try:
            repository.save(new_amenity)
            return jsonify({"Success": "Amenity added", "amenity": new_amenity.to_dict()}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    elif request.method == "GET":
        # Retrieve all amenities
        try:
            amenities = repository.get_all(Amenity)
            amenity_list = [{
                "id": amenity.id,
                "name": amenity.name
            } for amenity in amenities]
            return jsonify(amenity_list), 200
        except Exception as e:
            return jsonify({"Error": str(e)}), 500

@amenities("/amenities/<int:id>", methods=['GET', 'DELETE', 'PUT'])
@jwt_required()
def handle_amenity(id):
    """
    Retrieve, update, or delete a specific amenity by its ID.
    """
    amenity = repository.get(Amenity, id)

    if request.method == "GET":
        if amenity:
            return jsonify({
                "id": amenity.id,
                "name": amenity.name
            }), 200
        return jsonify({"Error": "Amenity not found"}), 404

    elif request.method == "DELETE":
        # Verify JWT and check admin rights
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({"msg": "Missing Authorization Header"}), 401

        claims = get_jwt()
        if claims.get('is_admin') is not True:
            return jsonify({"msg": "Administration rights required"}), 403

        if not amenity:
            return jsonify({"Error": "Amenity not found"}), 404
        try:
            repository.delete(amenity)
            return jsonify({"Success": "Amenity deleted"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    elif request.method == "PUT":
        if not amenity:
            return jsonify({"Error": "Amenity not found"}), 404

        amenity_data = request.get_json()
        amenity.name = amenity_data.get("name", amenity.name)
        try:
            repository.update(amenity)
            return jsonify({"Success": "Amenity updated"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
