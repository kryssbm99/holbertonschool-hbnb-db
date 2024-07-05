from flask import Blueprint, jsonify, request
from models.review import Review
from models.user import User
from models.place import Place
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.persistence.db import DBRepository

# Create Blueprint for review-related endpoints
review = Blueprint("review", __name__)
repository = DBRepository()

@review.route("/places/<string:id>/reviews", methods=["POST", "GET"])
@jwt_required()
def handle_place_review(id):
    """
    Handle creation and retrieval of reviews for a place.
    """
    if request.method == "POST":
        current_user = get_jwt_identity()
        if current_user:
            review_data = request.get_json()
            if not review_data:
                return jsonify({"Error": "Problem during review creation"}), 400

            user_id = review_data.get("user_id")
            rating = review_data.get("rating")
            comment = review_data.get("comment")

            if not isinstance(rating, int):
                return jsonify({"Error": "rating must be an integer."}), 400
            if not 1 <= rating <= 5:
                return jsonify({"Error": "rating must be between 1 and 5."}), 400
            if not isinstance(comment, str):
                return jsonify({"Error": "comment must be a string."}), 400

            # Validate user and place existence
            user = repository.get(User, user_id)
            if not user:
                return jsonify({"error": "User not found"}), 404
            place = repository.get(Place, id)
            if not place:
                return jsonify({"error": "No place found"}), 404

            # Check if user is not rating their own place
            if place.host_id == user_id:
                return jsonify({"error": "Can't rate your own place"}), 403

            # Check if user has already reviewed this place
            existing_review = Review.query.filter_by(user_id=user_id, place_id=id).first()
            if existing_review:
                return jsonify({"error": "You can't review the same place twice"}), 403

            new_review = Review(user_id=user_id, place_id=id, rating=rating, comment=comment)
            try:
                repository.save(new_review)
                return jsonify({"message": "Review added successfully", "review": new_review.to_dict()}), 201
            except Exception as e:
                return jsonify({"error": str(e)}), 500

    elif request.method == "GET":
        reviews = Review.query.filter_by(place_id=id).all()
        if reviews:
            reviews_list = [review.to_dict() for review in reviews]
            return jsonify(reviews_list), 200
        else:
            return jsonify({"error": "No reviews found for this place"}), 404

@review.route("/users/<string:id>/reviews", methods=['GET'])
@jwt_required()
def user_review(id):
    """
    Retrieve all reviews for a specific user.
    """
    try:
        user = repository.get(User, id)
        if not user:
            return jsonify({"error": "No user found"}), 404

        reviews = Review.query.filter_by(user_id=id).all()
        review_list = [review.to_dict() for review in reviews]
        return jsonify(review_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@review.route("/reviews/<string:id>", methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def review_info(id):
    """
    Retrieve, update, or delete a specific review.
    """
    try:
        review = repository.get(Review, id)
        if not review:
            return jsonify({"error": "No review found"}), 404

        if request.method == "GET":
            return jsonify(review.to_dict()), 200

        if request.method == "PUT":
            review_data = request.get_json()
            review.rating = review_data.get("rating", review.rating)
            review.comment = review_data.get("comment", review.comment)
            repository.update(review)
            return jsonify({"Success": "Review updated!", "review": review.to_dict()}), 200

        if request.method == "DELETE":
            repository.delete(review)
            return jsonify({"Success": "The review has been removed successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
