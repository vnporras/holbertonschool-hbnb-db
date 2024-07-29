"""
Places controller module
"""

from flask import abort
from flask_jwt_extended import jwt_required, current_user
from src.models.place import Place


def get_places():
    """Returns all places"""
    places: list[Place] = Place.get_all()

    return [place.to_dict() for place in places], 200


def get_place_by_id(place_id: str):
    """Returns a place by ID"""
    place: Place | None = Place.get(place_id)

    if not place:
        abort(404, f"Place with ID {place_id} not found")

    return place.to_dict(), 200


@jwt_required()
def create_place(data: dict):
    """Creates a new place"""

    if current_user.is_admin is False and current_user.id != data["host_id"]:
        abort(403, "Forbidden")

    try:
        place = Place.create(data | {"host_id": current_user.id})
    except ValueError as e:
        abort(404, str(e))

    return place.to_dict(), 201


@jwt_required()
def update_place(place_id: str, data: dict):
    """Updates a place by ID"""
    place: Place | None = Place.get(place_id)

    if not place:
        abort(404, f"Place with ID {place_id} not found")

    if place.host_id != current_user.id and not current_user.is_admin:
        abort(403, "Forbidden")

    # Remove the host_id from the data to avoid updating it
    data.pop("host_id", None)

    try:
        updated_place: Place = Place.update(place, data)
    except ValueError as e:
        abort(400, str(e))

    return updated_place.to_dict(), 200


@jwt_required()
def delete_place(place_id: str):
    """Deletes a place by ID"""
    place: Place | None = Place.get(place_id)

    if not place or place.host_id != current_user.id:
        abort(404, f"Place with ID {place_id} not found")

    Place.delete(place_id)

    return "", 204
