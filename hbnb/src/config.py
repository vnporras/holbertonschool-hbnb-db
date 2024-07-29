"""
This module exports configuration classes for the Flask application.

- DevelopmentConfig
- TestingConfig
- ProductionConfig

"""

from abc import ABC
from datetime import timedelta
import os
from dotenv import load_dotenv
from utils.constants import (
    REPOSITORY_ENV_VAR,
    DEFAULT_REPOSITORY,
    DATABASE_URL_ENV_VAR,
    Repos,
)


load_dotenv()


class Config(ABC):
    """
    Initial configuration settings
    This class should not be instantiated directly
    """

    DEBUG = False
    TESTING = False

    REPOSITORY = os.getenv(REPOSITORY_ENV_VAR, DEFAULT_REPOSITORY)

    JWT_SECRET_KEY = os.getenv("JWT_SECRET") or "you-will-never-guess"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)

    BCRYPT_LOG_ROUNDS = 12

    SWAGGER_UI_DOC_EXPANSION = "list"
    RESTX_VALIDATE = True

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}


class DevelopmentConfig(Config):
    """
    Development configuration settings
    This configuration is used when running the application locally

    This is useful for development and debugging purposes.

    To check if the application is running in development mode, you can use:
    ```
    app = Flask(__name__)

    if app.debug:
        # Do something
    ```
    """

    SQLALCHEMY_DATABASE_URI = os.getenv(
        DATABASE_URL_ENV_VAR,
        "sqlite:///hbnb_dev.db",
    )
    DEBUG = True


class TestingConfig(Config):
    """
    Testing configuration settings
    This configuration is used when running tests.
    You can enabled/disable things across the application

    To check if the application is running in testing mode, you can use:
    ```
    app = Flask(__name__)

    if app.testing:
        # Do something
    ```

    """

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    """
    Production configuration settings
    This configuration is used when you create a
    production build of the application

    The debug or testing options are disabled in this configuration.
    """

    REPOSITORY = Repos.DB.value

    TESTING = False
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = os.getenv(
        DATABASE_URL_ENV_VAR,
        "postgresql://user:password@localhost:5432/hbnb_prod",
    )

    # App should be served over HTTPS
    JWT_COOKIE_SECURE = True
