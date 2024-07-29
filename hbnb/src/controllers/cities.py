"""
Cities controller module
"""

from flask import abort
from src.models.city import City
from utils.decorators import admin_required


def get_cities():
    """Returns all cities"""
    cities: list[City] = City.get_all()

    return [city.to_dict() for city in cities]


def get_city_by_id(city_id: str):
    """Returns a city by ID"""
    city: City | None = City.get(city_id)

    if not city:
        abort(404, f"City with ID {city_id} not found")

    return city.to_dict()


@admin_required()
def create_city(data: dict):
    """Creates a new city"""
    try:
        city = City.create(data)
    except ValueError as e:
        abort(400, str(e))

    return city.to_dict(), 201


@admin_required()
def update_city(city_id: str, data: dict):
    """Updates a city by ID"""
    city: City | None = City.get(city_id)

    if not city:
        abort(404, f"City with ID {city_id} not found")

    try:
        updated_city: City = City.update(city, data)
    except ValueError as e:
        abort(400, str(e))

    return updated_city.to_dict()


@admin_required()
def delete_city(city_id: str):
    """Deletes a city by ID"""
    if not City.delete(city_id):
        abort(404, f"City with ID {city_id} not found")

    return "", 204
