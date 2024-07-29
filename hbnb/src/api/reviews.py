"""
This module contains the routes for the reviews blueprint
"""

from flask_restx import Namespace, Resource, fields
from src.api.base import base_fields
from src.controllers.reviews import (
    create_review,
    delete_review,
    get_reviews_from_place,
    get_reviews_from_user,
    get_review_by_id,
    get_reviews,
    update_review,
)

api = Namespace("Review", description="Review related operations")

review_input_fields = api.model(
    name="ReviewInput",
    model={
        "user_id": fields.String(description="User ID", required=True),
        "comment": fields.String(description="Comment", required=True),
        "rating": fields.Float(
            description="Rating", required=True, min=0, max=5
        ),
    },
)

review_fields = api.model(
    name="Review",
    model=base_fields.clone("Review", review_input_fields),
)


class ReviewList(Resource):
    """Handles HTTP requests to URL: /reviews"""

    @api.response(200, "Reviews found", [review_fields])
    def get(self):
        """Get all reviews"""
        return get_reviews()

    @api.expect(review_input_fields)
    @api.response(201, "Review created", review_fields)
    @api.response(400, "Bad request")
    def post(self):
        """Create a new review"""
        return create_review(api.payload)


@api.doc(params={"review_id": "The ID of the review"})
@api.response(404, "Review not found")
class Review(Resource):
    """Handles HTTP requests to URL: /reviews/<review_id>"""

    @api.response(200, "Review found", review_fields)
    def get(self, review_id: str):
        """Get a review by ID"""
        return get_review_by_id(review_id)

    @api.expect(review_input_fields)
    @api.response(200, "Review updated", review_fields)
    def put(self, review_id: str):
        """Update a review by ID"""
        return update_review(review_id, api.payload)

    @api.response(204, "Review deleted")
    def delete(self, review_id: str):
        """Delete a review by ID"""
        return delete_review(review_id)


class UserReviewList(Resource):
    """Handles HTTP requests to URL: /users/<user_id>/reviews"""

    @api.response(200, "Reviews found", [review_fields])
    def get(self, user_id: str):
        """Get all reviews from a user"""
        return get_reviews_from_user(user_id)


class PlaceReviewList(Resource):
    """Handles HTTP requests to URL: /places/<place_id>/reviews"""

    @api.response(200, "Reviews found", [review_fields])
    def get(self, place_id: str):
        """Get all reviews from a place"""
        return get_reviews_from_place(place_id)

    @api.expect(review_input_fields)
    @api.response(201, "Review created", review_fields)
    @api.response(400, "Bad request")
    def post(self, place_id: str):
        """Create a new review for a place"""
        return create_review(place_id, api.payload)


api.add_resource(ReviewList, "reviews")
api.add_resource(Review, "reviews/<review_id>")
api.add_resource(UserReviewList, "users/<user_id>/reviews")
api.add_resource(PlaceReviewList, "places/<place_id>/reviews")
