"""
Users controller module
"""

from flask import abort, request, jsonify, Blueprint
from src.models.user import User
from werkzeug.security import generate_password_hash
from src.models import db

# Create a Blueprint for the user-related endpoints
users_bp = Blueprint('users_bp', __name__)

@users_bp.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user.

    This endpoint allows the creation of a new user with a unique email and password.

    Returns:
        JSON: The newly created user's data or an error message if the user already exists.
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    # Check if the user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "User already exists"}), 400
   
    # Hash the password and create a new user
    hashed_password = generate_password_hash(password)
    new_user = User(email=email, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201

def get_user_by_id(user_id: str):
    """
    Get a user by ID.

    This function retrieves a user by their ID.

    Args:
        user_id (str): The ID of the user.

    Returns:
        JSON: The user's data or a 404 error if not found.
    """
    user = User.query.get(user_id)

    if not user:
        abort(404, f"User with ID {user_id} not found")

    return jsonify(user.to_dict()), 200

@users_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id: int):
    """
    Update a user by ID.

    This endpoint allows the update of a user's email and/or password.

    Args:
        user_id (int): The ID of the user.

    Returns:
        JSON: The updated user's data or an error message if the user is not found.
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    data = request.get_json()
    user.email = data.get('email', user.email)
    password = data.get('password')
    if password:
        user.password_hash = generate_password_hash(password)

    db.session.commit()

    return jsonify(user.to_dict()), 200

@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id: int):
    """
    Delete an existing user.

    This endpoint allows the deletion of a user by their ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        JSON: A message indicating the result of the operation.
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"msg": "User deleted"}), 200
