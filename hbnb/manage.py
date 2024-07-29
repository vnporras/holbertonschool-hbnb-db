""" Entry point for the application. """

from flask.cli import FlaskGroup
from src import create_app, db


cli = FlaskGroup(create_app=create_app)


@cli.command("recreate_db")
def create_db():
    """Create the database."""
    db.drop_all()
    db.create_all()
    print("Database created")


if __name__ == "__main__":
    cli()
