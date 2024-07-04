"""
Module defines authenticated endpoints.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.review import Review
from ..models import db

# Create a Blueprint for the authenticated endpoints
auth_endpoints_bp = Blueprint('auth_endpoints_bp', __name__)

@auth_endpoints_bp.route('/places/<int:place_id>/reviews', methods=['POST'])
@jwt_required()
def submit_review(place_id):
    """
    Submit a review for a place.

    This endpoint allows a logged-in user to submit a review for a specified place.

    Args:
        place_id (int): The ID of the place.

    Returns:
        JSON: The newly created review's data or an error message.
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Create a new review instance
    review = Review(text=data['text'], place_id=place_id, user_id=user_id)
    
    # Add and commit the new review to the database
    db.session.add(review)
    db.session.commit()
    
    return jsonify(review.to_dict()), 201

@auth_endpoints_bp.route('/places/<int:place_id>/reviews/<int:review_id>', methods=['PUT'])
@jwt_required()
def edit_review(place_id, review_id):
    """
    Edit a review.

    This endpoint allows a logged-in user to edit their review for a specified place.

    Args:
        place_id (int): The ID of the place.
        review_id (int): The ID of the review.

    Returns:
        JSON: The updated review's data or an error message.
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Retrieve the review from the database
    review = Review.query.filter_by(id=review_id, place_id=place_id, user_id=user_id).first()
    
    # Check if the review exists and update it
    if review:
        review.text = data['text']
        db.session.commit()
        return jsonify(review.to_dict()), 200
    else:
        return jsonify({"msg": "Review not found"}), 404

@auth_endpoints_bp.route('/places/<int:place_id}/reviews/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(place_id, review_id):
    """
    Delete a review.

    This endpoint allows a logged-in user to delete their review for a specified place.

    Args:
        place_id (int): The ID of the place.
        review_id (int): The ID of the review.

    Returns:
        JSON: A message indicating the result of the operation.
    """
    user_id = get_jwt_identity()
    
    # Retrieve the review from the database
    review = Review.query.filter_by(id=review_id, place_id=place_id, user_id=user_id).first()
    
    # Check if the review exists and delete it
    if review:
        db.session.delete(review)
        db.session.commit()
        return jsonify({"msg": "Review deleted successfully"}), 200
    else:
        return jsonify({"msg": "Review not found"}), 404
