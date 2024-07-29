"""
This module contains the routes for the countries endpoint
"""

from flask_restx import Namespace, Resource, fields
from src.controllers.countries import (
    get_countries,
    get_country_by_code,
    get_country_cities,
)

api = Namespace("Country", description="Country related operations")

country_fields = api.model(
    name="Country",
    model={
        "code": fields.String(description="Country code"),
        "name": fields.String(description="Country name"),
    },
)


class CountryList(Resource):
    """Handles HTTP requests to URL: /countries"""

    @api.response(200, "Countries found", [country_fields])
    def get(self):
        """Get all countries"""
        return get_countries()


class Country(Resource):
    """Handles HTTP requests to URL: /countries/<code>"""

    @api.response(200, "Country found", country_fields)
    @api.response(404, "Country not found")
    def get(self, code: str):
        """Get a country by code"""
        return get_country_by_code(code)


class CountryCities(Resource):
    """Handles HTTP requests to URL: /countries/<code>/cities"""

    @api.response(200, "Cities found", [country_fields])
    @api.response(404, "Country not found")
    def get(self, code: str):
        """Get all cities from a country"""
        return get_country_cities(code)


api.add_resource(CountryList, "/")
api.add_resource(Country, "/<code>")
api.add_resource(CountryCities, "/<code>/cities")
