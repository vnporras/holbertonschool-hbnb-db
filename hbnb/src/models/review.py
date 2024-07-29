"""
Review related functionality
"""

from src.models.base import Base
from src.models.place import Place
from src.models.user import User
from src import repo, db

import sqlalchemy as sa
import sqlalchemy.orm as so


class Review(Base, db.Model):
    """Review representation"""

    id: so.Mapped[str] = sa.Column(sa.String(255), primary_key=True)
    place_id: so.Mapped[str] = sa.Column(
        sa.String(255), sa.ForeignKey("place.id"), nullable=False
    )
    user_id: so.Mapped[str] = sa.Column(
        sa.String(255), sa.ForeignKey("user.id"), nullable=False
    )
    comment: so.Mapped[str] = sa.Column(sa.String(255), nullable=False)
    rating: so.Mapped[float] = sa.Column(sa.Float, nullable=False)

    place = so.relationship("Place", backref="reviews")

    def __init__(
        self, place_id: str, user_id: str, comment: str, rating: float, **kw
    ) -> None:
        """Dummy init"""
        super().__init__(**kw)

        self.place_id = place_id
        self.user_id = user_id
        self.comment = comment
        self.rating = rating

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<Review {self.id} - '{self.comment[:25]}...'>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "place_id": self.place_id,
            "user_id": self.user_id,
            "comment": self.comment,
            "rating": self.rating,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "Review":
        """Create a new review"""
        user: User | None = User.get(data["user_id"])

        if not user:
            raise ValueError(f"User with ID {data['user_id']} not found")

        place: Place | None = Place.get(data["place_id"])

        if not place:
            raise ValueError(f"Place with ID {data['place_id']} not found")

        new_review = Review(**data)

        repo.save(new_review)

        return new_review

    @staticmethod
    def update(review: "Review", data: dict) -> "Review":
        """Update an existing review"""
        for key, value in data.items():
            setattr(review, key, value)

        repo.update(review)

        return review
