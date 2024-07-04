"""
Module defines public endpoints.
"""

from flask import Blueprint, jsonify
from ..models.place import Place

# Create a Blueprint for the public endpoints
public_endpoints_bp = Blueprint('public_endpoints_bp', __name__)

@public_endpoints_bp.route('/places', methods=['GET'])
def view_places():
    """
    View all places.

    This endpoint allows anyone to view a list of all places.

    Returns:
        JSON: A list of all places.
    """
    # Query all places from the database
    places = Place.query.all()
    
    # Convert each place to a dictionary and return as JSON
    return jsonify([place.to_dict() for place in places]), 200

public_endpoints_bp.route('/places/<int:place_id>', methods=['GET'])
def view_place_details(place_id):
    """
    View the details of a specific place.

    This endpoint allows anyone to view the details of a specific place by its ID.

    Args:
        place_id (int): The ID of the place.

    Returns:
        JSON: The details of the specified place or an error message if not found.
    """
    # Query the place by ID from the database
    place = Place.query.get(place_id)
    
    # Check if the place exists and return its details
    if place:
        return jsonify(place.to_dict()), 200
    else:
        return jsonify({"msg": "Place not found"}), 404
