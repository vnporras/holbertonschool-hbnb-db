"""
This module contains the routes for the users endpoints.
"""

from flask_restx import Namespace, Resource, fields
from src.api.base import base_fields
from src.controllers.users import (
    create_user,
    delete_user,
    get_user_by_id,
    get_users,
    update_user,
)

api = Namespace("User", description="User related operations")

user_input_fields = api.model(
    name="UserInput",
    model={
        "email": fields.String(description="Email of the user", required=True),
        "password": fields.String(description="Password", required=True),
        "first_name": fields.String(
            description="First name of the user", required=True
        ),
        "last_name": fields.String(
            description="Last name of the user",
            required=True,
        ),
        "is_admin": fields.Boolean(
            description="Admin status of the user",
            required=False,
            default=False,
        ),
    },
)

user_fields = api.model(
    name="User",
    model=base_fields.clone("User", user_input_fields),
)


class UserList(Resource):
    """Handles HTTP requests to URL: /users"""

    @api.response(200, "Users found", [user_fields])
    def get(self):
        """Get all users"""
        return get_users()

    @api.expect(user_input_fields)
    @api.response(201, "User created", user_fields)
    @api.response(400, "Bad request")
    def post(self):
        """Create a new user"""
        return create_user(api.payload)


@api.doc(params={"user_id": "The ID of the user"})
@api.response(404, "User not found")
class User(Resource):
    """Handles HTTP requests to URL: /users/<user_id>"""

    @api.response(200, "User found", user_fields)
    def get(self, user_id: str):
        """Get a user by ID"""
        return get_user_by_id(user_id)

    # expect partial updates
    @api.expect(user_input_fields)
    @api.response(200, "User updated", user_fields)
    def put(self, user_id: str):
        """Update a user by ID"""
        return update_user(user_id, api.payload)

    @api.response(204, "User deleted")
    def delete(self, user_id: str):
        """Delete a user by ID"""
        return delete_user(user_id)


api.add_resource(UserList, "/")
api.add_resource(User, "/<user_id>")
