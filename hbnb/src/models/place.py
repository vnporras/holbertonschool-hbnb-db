"""
Place related functionality
"""

from src.models.base import Base
from src.models.city import City
from src.models.user import User

from typing import Optional
from src import repo, db

import sqlalchemy as sa
import sqlalchemy.orm as so


class Place(Base, db.Model):
    """Place representation"""

    id: so.Mapped[str] = sa.Column(sa.String(255), primary_key=True)
    name: so.Mapped[str] = sa.Column(sa.String(255), nullable=False)
    description: so.Mapped[Optional[str]] = sa.Column(
        sa.String(255),
        nullable=False,
    )
    address: so.Mapped[str] = sa.Column(sa.String(255), nullable=False)
    latitude: so.Mapped[float] = sa.Column(sa.Float, nullable=False)
    longitude: so.Mapped[float] = sa.Column(sa.Float, nullable=False)
    host_id: so.Mapped[str] = sa.Column(
        sa.String(255), sa.ForeignKey("user.id"), nullable=False
    )
    city_id: so.Mapped[str] = sa.Column(
        sa.String(255), sa.ForeignKey("city.id"), nullable=False
    )
    price_per_night: so.Mapped[int] = sa.Column(sa.Integer, nullable=False)
    number_of_rooms: so.Mapped[int] = sa.Column(sa.Integer, nullable=False)
    number_of_bathrooms: so.Mapped[int] = sa.Column(sa.Integer, nullable=False)
    max_guests: so.Mapped[int] = sa.Column(sa.Integer, nullable=False)

    host = so.relationship("User", backref="places")
    city = so.relationship("City", backref="places")

    def __init__(self, data: dict | None = None, **kw) -> None:
        """Dummy init"""
        super().__init__(**kw)

        if not data:
            return

        self.name = data.get("name", "")
        self.description = data.get("description", "")
        self.address = data.get("address", "")
        self.city_id = data["city_id"]
        self.latitude = float(data.get("latitude", 0.0))
        self.longitude = float(data.get("longitude", 0.0))
        self.host_id = data["host_id"]
        self.price_per_night = int(data.get("price_per_night", 0))
        self.number_of_rooms = int(data.get("number_of_rooms", 0))
        self.number_of_bathrooms = int(data.get("number_of_bathrooms", 0))
        self.max_guests = int(data.get("max_guests", 0))

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<Place {self.id} ({self.name})>"

    def to_dict(self, include=False) -> dict:
        """Dictionary representation of the object"""



        d = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "city_id": self.city_id,
            "host_id": self.host_id,
            "price_per_night": self.price_per_night,
            "number_of_rooms": self.number_of_rooms,
            "number_of_bathrooms": self.number_of_bathrooms,
            "max_guests": self.max_guests,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "host": self.host.to_dict(),
        }

        if include:
            d["city"] = self.city.to_dict()

        return d

    @staticmethod
    def create(data: dict) -> "Place":
        """Create a new place"""
        user: User | None = User.get(data["host_id"])

        if not user:
            raise ValueError(f"User with ID {data['host_id']} not found")

        city: City | None = City.get(data["city_id"])

        if not city:
            raise ValueError(f"City with ID {data['city_id']} not found")

        new_place = Place(data=data)

        repo.save(new_place)

        return new_place

    @staticmethod
    def update(place: "Place", data: dict) -> "Place":
        """Update an existing place"""

        for key, value in data.items():
            setattr(place, key, value)

        repo.update(place)

        return place
