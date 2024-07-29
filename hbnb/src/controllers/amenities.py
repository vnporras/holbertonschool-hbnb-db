"""
Amenity controller module
"""

from flask import abort
from flask_jwt_extended import jwt_required
from src.models.amenity import Amenity
from utils.decorators import admin_required


def get_amenities():
    """Returns all amenities"""
    amenities: list[Amenity] = Amenity.get_all()

    return [amenity.to_dict() for amenity in amenities]


def get_amenity_by_id(amenity_id: str):
    """Returns a amenity by ID"""
    amenity: Amenity | None = Amenity.get(amenity_id)

    if not amenity:
        abort(404, f"Amenity with ID {amenity_id} not found")

    return amenity.to_dict()


@admin_required()
def create_amenity(data: dict):
    """Creates a new amenity"""
    try:
        amenity = Amenity.create(data)
    except ValueError as e:
        abort(400, str(e))

    return amenity.to_dict(), 201


@admin_required()
def update_amenity(amenity_id: str, data: dict):
    """Updates a amenity by ID"""
    updated_amenity: Amenity | None = Amenity.update(amenity_id, data)

    if not updated_amenity:
        abort(404, f"Amenity with ID {amenity_id} not found")

    return updated_amenity.to_dict()


@admin_required()
def delete_amenity(amenity_id: str):
    """Deletes a amenity by ID"""
    if not Amenity.delete(amenity_id):
        abort(404, f"Amenity with ID {amenity_id} not found")

    return "", 204
