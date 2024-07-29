"""
Reviews controller module
"""

from flask import abort
from flask_jwt_extended import current_user, jwt_required
from src.models.review import Review
from utils.decorators import admin_required


def get_reviews():
    """Returns all reviews"""
    reviews = Review.get_all()

    return [review.to_dict() for review in reviews], 200


@jwt_required()
def create_review(place_id: str, data: dict):
    """Creates a new review"""

    if current_user.is_admin is False and current_user.id != data["user_id"]:
        abort(403, "Forbidden")

    try:
        review = Review.create(
            data
            | {
                "place_id": place_id,
                "user_id": current_user.id,
            }
        )
    except ValueError as e:
        abort(400, str(e))

    return review.to_dict(), 201


def get_reviews_from_place(place_id: str):
    """Returns all reviews from a specific place"""
    reviews: list[Review] = Review.get_all()

    return (
        [
            review.to_dict()
            for review in reviews
            if review.place_id == place_id
        ],
        200,
    )


@admin_required()
def get_reviews_from_user(user_id: str):
    """Returns all reviews from a specific user"""
    reviews: list[Review] = Review.get_all()

    return (
        [review.to_dict() for review in reviews if review.user_id == user_id],
        200,
    )


def get_review_by_id(review_id: str):
    """Returns a review by ID"""
    review: Review | None = Review.get(review_id)

    if not review:
        abort(404, f"Review with ID {review_id} not found")

    return review.to_dict(), 200


@jwt_required()
def update_review(review_id: str, data: dict):
    """Updates a review by ID"""

    review: Review | None = Review.get(review_id)

    if not review or review.user_id != current_user.id:
        abort(404, f"Review with ID {review_id} not found")

    data.pop("user_id", None)

    try:
        updated_review: Review = Review.update(review, data)
    except ValueError as e:
        abort(400, str(e))

    return updated_review.to_dict(), 200


@jwt_required()
def delete_review(review_id: str):
    """Deletes a review by ID"""
    if not Review.delete(review_id):
        abort(404, f"Review with ID {review_id} not found")

    return "", 204
