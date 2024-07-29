"""
This module contains the routes for the amenities blueprint
"""

from flask_restx import Namespace, Resource, fields
from src.api.base import base_fields
from src.controllers.amenities import (
    create_amenity,
    delete_amenity,
    get_amenity_by_id,
    get_amenities,
    update_amenity,
)

api = Namespace("Amenity", description="Amenity related operations")

amenity_input_fields = api.model(
    name="AmenityInput",
    model={
        "name": fields.String(description="Name of the amenity", min_length=2),
    },
)

amenity_fields = api.model(
    name="Amenity", model=base_fields.clone("Amenity", amenity_input_fields)
)


class AmenityList(Resource):
    """Handles HTTP requests to URL: /amenities"""

    @api.response(200, "Amenities found", [amenity_fields])
    def get(self):
        """Get all amenities"""
        return get_amenities()

    @api.expect(amenity_input_fields)
    @api.response(201, "Amenity created", amenity_fields)
    @api.response(400, "Bad request")
    def post(self):
        """Create a new amenity"""
        return create_amenity(api.payload)


@api.doc(params={"amenity_id": "The ID of the amenity"})
@api.response(404, "Amenity not found")
class Amenity(Resource):
    """Handles HTTP requests to URL: /amenities/<amenity_id>"""

    @api.response(200, "Amenity found", amenity_fields)
    def get(self, amenity_id: str):
        """Get an amenity by ID"""
        return get_amenity_by_id(amenity_id)

    @api.expect(amenity_input_fields)
    @api.response(200, "Amenity updated", amenity_fields)
    def put(self, amenity_id: str):
        """Update an amenity by ID"""
        return update_amenity(amenity_id, api.payload)

    @api.response(204, "Amenity deleted")
    def delete(self, amenity_id: str):
        """Delete an amenity by ID"""
        return delete_amenity(amenity_id)


api.add_resource(AmenityList, "/")
api.add_resource(Amenity, "/<amenity_id>")
