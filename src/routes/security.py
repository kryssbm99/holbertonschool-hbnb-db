"""
Module for authentication security routes.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.models.user import User, db

# Create a Blueprint for the security endpoints
security_bp = Blueprint('security_bp', __name__)

@security_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    
    This endpoint allows a new user to register by providing user data.
    """
    data = request.get_json()
    user = User.create(data)
    return jsonify(user.to_dict()), 201

@security_bp.route('/login', methods=['POST'])
def login():
    """
    Log in a user.
    
    This endpoint allows an existing user to log in by providing email and password.
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()

    # Check if the user exists and the password is correct
    if user and user.check_password(password):
        # Create an access token with additional claims
        access_token = create_access_token(identity=user.id, additional_claims={"is_admin": user.is_admin})
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad email or password"}), 401

@security_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    """
    Access a protected route.
    
    This endpoint can only be accessed by authenticated users.
    """
    current_user = get_jwt_identity()
    return jsonify(message="This is a protected route", user=current_user), 200

@security_bp.route('/promote_user', methods=['POST'])
@jwt_required()
def promote_user():
    """
    Promote a user to admin.
    
    This endpoint allows an admin to promote another user to admin status.
    """
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    # Check if the current user is an admin
    if not current_user or not current_user.is_admin:
        return jsonify({'message': 'Access forbidden'}), 403

    data = request.get_json()
    email = data.get('email')
    user = User.query.filter_by(email=email).first()

    # Check if the user to be promoted exists
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Promote the user to admin
    user.is_admin = True
    db.session.commit()

    return jsonify({'message': 'User promoted to admin'}), 200
