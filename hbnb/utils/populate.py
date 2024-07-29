""" Populate the database with some data at the start of the application"""

from flask_sqlalchemy import SQLAlchemy
from src.persistence.repository import Repository
import csv


def populate_memory(repo: Repository) -> None:
    """Populates the db with a dummy country"""
    from src.models.country import Country

    countries = [
        Country(name="Uruguay", code="UY"),
    ]

    for country in countries:
        repo.save(country)


def populate_db(db: SQLAlchemy) -> None:
    """Populate the database with some data at the start of the application"""
    from src.models.country import Country

    if Country.query.first():
        print("DB already populated")
        return

    with open("utils/countries.csv") as file:
        reader = csv.reader(file, delimiter="\t")

        countries = [Country(name=row[0], code=row[1]) for row in reader]

        db.session.add_all(countries)
        db.session.commit()
