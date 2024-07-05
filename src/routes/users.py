"""
This module defines user-related endpoints.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from ..models.user import User
from ..models import db

# Create a Blueprint for the user-related endpoints
users_bp = Blueprint('users_bp', __name__)


@users_bp.route('/users', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_user():
    """
    Create a new user.

    This endpoint allows a logged-in user to create a new user.

    Returns:
        JSON: The newly created user's data or an error message.
    """
    data = request.get_json()

    # Create a new user instance
    user = User.create(data)

    return jsonify(user.to_dict()), 201


@users_bp.route('/users/<int:user_id>/', methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_user(user_id):
    """
    Update an existing user.

    This endpoint allows a logged-in user to update an existing user's details.

    Args:
        user_id (int): The ID of the user.

    Returns:
        JSON: The updated user's data or an error message.
    """
    data = request.get_json()

    # Retrieve the user from the database
    user = User.query.get(user_id)

    # Check if the user exists and update the details
    if user:
        user.email = data.get('email', user.email)
        user.is_admin = data.get('is_admin', user.is_admin)
        if 'password' in data:
            user.password_hash = generate_password_hash(data['password'])
        db.session.commit()
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({"msg": "User not found"}), 404


@users_bp.route('/users/<int:user_id>/', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_user(user_id):
    """
    Delete a user.

    This endpoint allows a logged-in user to delete an existing user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        JSON: A message indicating the result of the operation.
    """
    user = User.query.get(user_id)

    # Check if the user exists and delete it
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"msg": "User deleted successfully"}), 200
    else:
        return jsonify({"msg": "User not found"}), 404


@users_bp.route('/users/<int:user_id>/', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_user(user_id):
    """
    Fetch a single user by ID.

    This endpoint allows a logged-in user to fetch details of a user by ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        JSON: The user's data or an error message.
    """
    # Retrieve the user from the database
    user = User.query.get(user_id)

    # Check if the user exists and return the details
    if user:
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({"msg": "User not found"}), 404


@users_bp.route('/users/', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_users():
    """
    Fetch all users.

    This endpoint allows a logged-in user to fetch details of all users.

    Returns:
        JSON: A list of all users.
    """
    # Retrieve all users from the database
    users = User.query.all()

    # Convert each user to a dictionary and return as JSON
    return jsonify([user.to_dict() for user in users]), 200
