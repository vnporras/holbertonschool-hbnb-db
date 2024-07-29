"""
User related functionality
"""

from src.models.base import Base
from src import repo, db, bcrypt

import sqlalchemy as sa
import sqlalchemy.orm as so


class User(Base, db.Model):
    """User representation"""
    id: so.Mapped[str] = sa.Column(sa.String(255), primary_key=True)
    email: so.Mapped[str] = sa.Column(sa.String(255), nullable=False, unique=True)
    password: so.Mapped[str] = sa.Column(sa.String(255), nullable=False)
    first_name: so.Mapped[str] = sa.Column(sa.String(255), nullable=False)
    last_name: so.Mapped[str] = sa.Column(sa.String(255), nullable=False)
    is_admin: so.Mapped[bool] = sa.Column(sa.Boolean, default=False)

    def __init__(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        is_admin: bool = False,
        **kw,
    ):
        """Dummy init"""
        super().__init__(**kw)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin

        self.set_password(password)

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<User {self.id} ({self.email})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        d = {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_admin": self.is_admin,
        }

        return d

    @staticmethod
    def create(user: dict) -> "User":
        """Create a new user"""
        users: list["User"] = User.get_all()

        for u in users:
            if u.email == user["email"]:
                raise ValueError("User already exists")

        new_user = User(**user)

        repo.save(new_user)

        return new_user

    @staticmethod
    def update(user_id: str, data: dict) -> "User | None":
        """Update an existing user"""
        user: User | None = User.get(user_id)

        if not user:
            return None

        if "email" in data:
            user.email = data["email"]
        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]

        repo.update(user)

        return user

    @staticmethod
    def get_by_email(email: str) -> "User | None":
        """Get a user by email"""
        users: list["User"] = User.get_all()

        for user in users:
            if user.email == email:
                return user

        return None

    def set_password(self, password: str) -> None:
        """Set the password"""
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")
