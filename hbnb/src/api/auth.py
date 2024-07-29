""" Api module for authentication """

from flask_restx import Namespace, Resource, fields

from src.controllers.auth import login, verify


api = Namespace("Auth", description="Authentication related operations")

login_fields = api.model(
    name="Login",
    model={
        "email": fields.String(description="User email", required=True),
        "password": fields.String(description="User password", required=True),
    },
)


class Login(Resource):
    """Handles HTTP requests to URL: /auth/login"""

    @api.expect(login_fields)
    @api.response(200, "Login successful")
    @api.response(401, "Unauthorized")
    def post(self):
        """Login a user"""
        return login(api.payload)

    @api.response(200, "User is logged in")
    @api.response(401, "Unauthorized")
    def get(self):
        """Verify whether a user is logged in or not"""
        return verify()


api.add_resource(Login, "/")
