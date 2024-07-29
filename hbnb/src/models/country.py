"""
Country related functionality
"""

from src import repo, db

import sqlalchemy as sa
import sqlalchemy.orm as so


class Country(db.Model):
    """
    Country representation

    This class does NOT inherit from Base, you can't delete or update a country

    This class is used to get and list countries
    """

    name: so.Mapped[str] = sa.Column(sa.String(255), nullable=False, unique=True)
    code: so.Mapped[str] = sa.Column(sa.String(2), primary_key=True)

    cities = so.relationship("City", back_populates="country")

    def __init__(self, name: str, code: str, **kw) -> None:
        """Dummy init"""
        super().__init__(**kw)
        self.name = name

        if type(code) is not str or len(code) != 2:
            raise ValueError("Code must be a 2-letter string")

        self.code = code

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<Country {self.code} ({self.name})>"

    def to_dict(self) -> dict:
        """Returns the dictionary representation of the country"""
        return {
            "name": self.name,
            "code": self.code,
        }

    @staticmethod
    def get_all() -> list["Country"]:
        """Get all countries"""
        countries: list["Country"] = repo.get_all("Country")

        return countries

    @staticmethod
    def get(code: str) -> "Country | None":
        """Get a country by its code"""
        for country in Country.get_all():
            if country.code == code:
                return country
        return None

    @staticmethod
    def create(name: str, code: str) -> "Country":
        """Create a new country"""
        country = Country(name, code)

        repo.save(country)

        return country
