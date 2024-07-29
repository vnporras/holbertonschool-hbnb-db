"""
Countries controller module
"""

from flask import abort
from src.models.city import City
from src.models.country import Country


def get_countries():
    """Returns all countries"""
    countries: list[Country] = Country.get_all()

    return [country.to_dict() for country in countries]


def get_country_by_code(code: str):
    """Returns a country by code"""
    country: Country | None = Country.get(code)

    if not country:
        abort(404, f"Country with ID {code} not found")

    return country.to_dict()


def get_country_cities(code: str):
    """Returns all cities for a specific country by code"""
    country: Country | None = Country.get(code)

    if not country:
        abort(404, f"Country with ID {code} not found")

    cities: list[City] = City.get_all()

    country_cities = [
        city.to_dict() for city in cities if city.country_code == country.code
    ]

    return country_cities
