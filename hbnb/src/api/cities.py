"""
This module contains the routes for the cities blueprint
"""

from flask_restx import Namespace, Resource, fields
from src.api.base import base_fields
from src.controllers.cities import (
    create_city,
    delete_city,
    get_city_by_id,
    get_cities,
    update_city,
)

api = Namespace("City", description="City related operations")

city_input_fields = api.model(
    name="CityInput",
    model={
        "name": fields.String(description="Name of the city", min_length=2),
        "country_code": fields.String(description="Country code of the city"),
    },
)

city_fields = api.model(
    name="City", model=base_fields.clone("City", city_input_fields)
)


class CityList(Resource):
    """Handles HTTP requests to URL: /cities"""

    @api.response(200, "Cities found", [city_fields])
    def get(self):
        """Get all cities"""
        return get_cities()

    @api.expect(city_input_fields)
    @api.response(201, "City created", city_fields)
    @api.response(400, "Bad request")
    def post(self):
        """Create a new city"""
        return create_city(api.payload)


@api.doc(params={"city_id": "The ID of the city"})
@api.response(404, "City not found")
class City(Resource):
    """Handles HTTP requests to URL: /cities/<city_id>"""

    @api.response(200, "City found", city_fields)
    def get(self, city_id: str):
        """Get a city by ID"""
        return get_city_by_id(city_id)

    @api.expect(city_input_fields)
    @api.response(200, "City updated", city_fields)
    def put(self, city_id: str):
        """Update a city by ID"""
        return update_city(city_id, api.payload)

    @api.response(204, "City deleted")
    def delete(self, city_id: str):
        """Delete a city by ID"""
        return delete_city(city_id)


api.add_resource(CityList, "/")
api.add_resource(City, "/<city_id>")
