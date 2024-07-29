"""
Amenity related functionality
"""

from src.models.base import Base
from src import repo, db

import sqlalchemy as sa
import sqlalchemy.orm as so


class Amenity(Base, db.Model):
    """Amenity representation"""

    id: so.Mapped[str] = sa.Column(sa.String(255), primary_key=True)
    name: so.Mapped[str] = sa.Column(sa.String(255), nullable=False, unique=True)

    def __init__(self, name: str, **kw) -> None:
        """Dummy init"""
        super().__init__(**kw)

        self.name = name

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<Amenity {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "Amenity":
        """Create a new amenity"""

        amenities: list["Amenity"] = Amenity.get_all()

        for u in amenities:
            if u.name == data["name"]:
                raise ValueError("Amenity already exists")

        amenity = Amenity(**data)

        repo.save(amenity)

        return amenity

    @staticmethod
    def update(amenity_id: str, data: dict) -> "Amenity | None":
        """Update an existing amenity"""
        amenity: Amenity | None = Amenity.get(amenity_id)

        if not amenity:
            return None

        if "name" in data:
            amenity.name = data["name"]

        repo.update(amenity)

        return amenity


class PlaceAmenity(Base, db.Model):
    """PlaceAmenity representation"""

    id: so.Mapped[str] = sa.Column(sa.String(255), primary_key=True)
    place_id: so.Mapped[str] = sa.Column(sa.String(255), sa.ForeignKey("place.id"))
    amenity_id: so.Mapped[str] = sa.Column(
        sa.String(255),
        sa.ForeignKey("amenity.id"),
    )

    place = so.relationship("Place", backref="amenities")
    amenity = so.relationship("Amenity", backref="places")

    def __init__(self, place_id: str, amenity_id: str, **kw) -> None:
        """Dummy init"""
        super().__init__(**kw)

        self.place_id = place_id
        self.amenity_id = amenity_id

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<PlaceAmenity ({self.place_id} - {self.amenity_id})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "place_id": self.place_id,
            "amenity_id": self.amenity_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def get(place_id: str, amenity_id: str) -> "PlaceAmenity | None":
        """Get a PlaceAmenity object by place_id and amenity_id"""
        place_amenities: list[PlaceAmenity] = repo.get_all("placeamenity")

        for place_amenity in place_amenities:
            if (
                place_amenity.place_id == place_id
                and place_amenity.amenity_id == amenity_id
            ):
                return place_amenity

        return None

    @staticmethod
    def create(data: dict) -> "PlaceAmenity":
        """Create a new PlaceAmenity object"""
        new_place_amenity = PlaceAmenity(**data)

        repo.save(new_place_amenity)

        return new_place_amenity

    @staticmethod
    def delete(place_id: str, amenity_id: str) -> bool:
        """Delete a PlaceAmenity object by place_id and amenity_id"""
        place_amenity = PlaceAmenity.get(place_id, amenity_id)

        if not place_amenity:
            return False

        repo.delete(place_amenity)

        return True

    @staticmethod
    def update(entity_id: str, data: dict):
        """Not implemented, isn't needed"""
        raise NotImplementedError(
            "This method is defined only because of the Base class"
        )
