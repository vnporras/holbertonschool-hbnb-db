"""
Cities controller module
"""

from flask import abort
from flask_jwt_extended import (
    create_access_token,
    current_user,
    jwt_required,
)
from src import bcrypt
from src.models.user import User
from utils.functions import validate_email


def login(data: dict):
    """Login a user"""
    email: str = data.get("email")
    password: str = data.get("password")

    valid_email = validate_email(email)

    if not valid_email:
        abort(401, "Invalid email or password")

    user = User.get_by_email(valid_email)

    if not user or not bcrypt.check_password_hash(user.password, password):
        abort(401, "Invalid email or password")

    aditional_claims = {"is_admin": user.is_admin}

    access_token = create_access_token(
        identity=user, additional_claims=aditional_claims
    )

    return access_token, 200


@jwt_required()
def verify():
    """Verify a user"""
    return {"logged_in_as": current_user.to_dict()}, 200
