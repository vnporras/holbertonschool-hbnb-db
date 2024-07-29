"""
This module contains the routes for the places blueprint
"""

from flask_restx import Namespace, Resource, fields
from src.api.base import base_fields
from src.controllers.places import (
    create_place,
    delete_place,
    get_place_by_id,
    get_places,
    update_place,
)

api = Namespace("Place", description="Places related operations")

places_input_fields = api.model(
    name="PlaceInput",
    model={
        "name": fields.String(
            description="Name of the place", min_length=2, required=True
        ),
        "description": fields.String(description="Description of the place"),
        "address": fields.String(
            description="Address of the place", required=True
        ),
        "latitude": fields.Float(description="Latitude", required=True),
        "longitude": fields.Float(description="Longitude", required=True),
        "host_id": fields.String(description="User ID", required=True),
        "city_id": fields.String(description="City ID", required=True),
        "number_of_rooms": fields.Integer(
            description="Number of rooms", min=1, required=True
        ),
        "number_of_bathrooms": fields.Integer(
            description="Number of bathrooms", min=0, required=True
        ),
        "max_guests": fields.Integer(
            description="Max number of guests", min=0, required=True
        ),
        "price_per_night": fields.Integer(
            description="Price per night", min=0, required=True
        ),
    },
)

place_fields = api.model(
    name="Place", model=base_fields.clone("Place", places_input_fields)
)


class PlaceList(Resource):
    """Handles HTTP requests to URL: /places"""

    @api.response(200, "Places found", [place_fields])
    def get(self):
        """Get all places"""
        return get_places()

    @api.expect(places_input_fields)
    @api.response(201, "Place created", place_fields)
    @api.response(400, "Bad request")
    def post(self):
        """Create a new place"""
        return create_place(api.payload)


@api.doc(params={"place_id": "The ID of the place"})
@api.response(404, "Place not found")
class Place(Resource):
    """Handles HTTP requests to URL: /places/<place_id>"""

    @api.response(200, "Place found", place_fields)
    def get(self, place_id: str):
        """Get a place by ID"""
        return get_place_by_id(place_id)

    @api.expect(places_input_fields)
    @api.response(200, "Place updated", place_fields)
    def put(self, place_id: str):
        """Update a place by ID"""
        return update_place(place_id, api.payload)

    @api.response(204, "Place deleted")
    def delete(self, place_id: str):
        """Delete a place by ID"""
        return delete_place(place_id)


api.add_resource(PlaceList, "/")
api.add_resource(Place, "/<place_id>")
