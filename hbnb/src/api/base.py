""" Exports the base fields for the API """

from flask_restx import fields, model

base_fields = model.Model(
    "Base",
    {
        "id": fields.String(description="The ID of the object"),
        "created_at": fields.DateTime(
            description="The creation date of the object"
        ),
        "updated_at": fields.DateTime(
            description="The last update date of the object"
        ),
    },
)
