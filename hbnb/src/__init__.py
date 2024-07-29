""" Initialize the Flask app. """

from typing import Optional
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from src.persistence.repository import RepositoryManager
from utils.constants import Repos
from utils.populate import populate_db

cors = CORS()
repo = RepositoryManager()
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(config_class="src.config.DevelopmentConfig") -> Flask:
    """
    Create a Flask app with the given configuration class.
    The default configuration class is DevelopmentConfig.
    """
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    app.config.from_object(config_class)

    models = get_models()

    register_extensions(app, models)
    register_routes(app)
    register_handlers(app)

    if app.debug:
        print(f"Using {repo.repo} repository")

    if app.config["REPOSITORY"] == Repos.DB.value:
        with app.app_context():
            db.create_all()
            populate_db(db)

    return app


def get_models() -> list:
    """Register the models in the repository manager"""
    from src.models.user import User
    from src.models.country import Country
    from src.models.city import City
    from src.models.amenity import Amenity
    from src.models.place import Place
    from src.models.review import Review

    return [User, Country, City, Amenity, Place, Review]


def register_extensions(app: Flask, models: Optional[list] = None) -> None:
    """Register the extensions for the Flask app"""
    db.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": "*"}})
    repo.init_app(app, models)
    bcrypt.init_app(app)
    jwt.init_app(app)
    # Further extensions can be added here


def register_routes(app: Flask) -> None:
    """Import and register the routes for the Flask app"""

    # Import the routes here to avoid circular imports
    from src.api import api_bp

    # Register the blueprints in the app
    app.register_blueprint(api_bp)


def register_handlers(app: Flask) -> None:
    """Register the error handlers for the Flask app."""
    from src.models.user import User

    app.errorhandler(404)(
        lambda e: ({"error": "Not found", "message": str(e)}, 404)
    )
    app.errorhandler(400)(
        lambda e: ({"error": "Bad request", "message": str(e)}, 400)
    )

    @jwt.user_identity_loader
    def identity_loader(user: User):
        """Loads the identity of the user for the JWT token decorator"""
        return user.id

    @jwt.user_lookup_loader
    def lookup_loader(_, jwt_data):
        """Retrieves and loads the user from the JWT token"""
        return User.get(jwt_data["sub"])
