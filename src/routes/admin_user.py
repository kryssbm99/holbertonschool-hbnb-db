"""
Admin user management endpoints.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from ..models.user import User
from ..models import db

# Create a Blueprint for the admin user management endpoints
admin_users_bp = Blueprint('admin_users_bp', __name__)

@admin_users_bp.route('/admin/users', methods=['POST'])
@jwt_required()
def promote_user():
    """
    Promote a user to admin.

    This endpoint handles POST requests to promote a user to admin status.
    It requires the requesting user to have administrative rights.
    """
    # Get the JWT claims to verify admin rights
    claims = get_jwt()

    # Check if the requesting user has admin rights
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403

    # Get the user data from the request
    data = request.get_json()
    user_id = data.get('user_id')

    # Retrieve the user from the database
    user = User.query.get(user_id)

    # Check if the user exists
    if user:
        # Promote the user to admin
        user.is_admin = True
        db.session.commit()
        return jsonify({"msg": "User promoted to admin successfully"}), 200
    else:
        return jsonify({"msg": "User not found"}), 404