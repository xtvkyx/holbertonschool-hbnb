"""User endpoints (API v1)."""
from __future__ import annotations

from flask import request
from flask_restx import Namespace, Resource, fields

from hbnb.facade import get_facade
facade = get_facade()


users_api = Namespace("users", description="User management endpoints")



# --- serializers (password excluded) ---
user_output = users_api.model(
    "UserOutput",
    {
        "id": fields.String,
        "first_name": fields.String,
        "last_name": fields.String,
        "email": fields.String,
        "is_admin": fields.Boolean,
        "created_at": fields.String,
        "updated_at": fields.String,
    },
)

user_create = users_api.model(
    "UserCreate",
    {
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
        "email": fields.String(required=True),
        "password": fields.String(required=True),
        "is_admin": fields.Boolean(required=False),
    },
)

user_update = users_api.model(
    "UserUpdate",
    {
        "first_name": fields.String(required=False),
        "last_name": fields.String(required=False),
        "email": fields.String(required=False),
        # password intentionally excluded
    },
)


def _public_user_dict(user):
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "is_admin": getattr(user, "is_admin", False),
        "created_at": user.created_at.isoformat() if hasattr(getattr(user, "created_at", None), "isoformat") else getattr(user, "created_at", None),
	"updated_at": user.updated_at.isoformat() if hasattr(getattr(user, "updated_at", None), "isoformat") else getattr(user, "updated_at", None),

    }


@users_api.route("/")
class UsersCollection(Resource):
    @users_api.expect(user_create)
    @users_api.response(201, "User created", user_output)
    @users_api.response(400, "Bad request")
    @users_api.response(409, "Email already exists")
    def post(self):
        """Create a user."""
        data = request.get_json(silent=True) or {}

        try:
            user = facade.create_user(data)
        except ValueError as e:
            # handle unique email error as conflict
            msg = str(e)
            if "must be unique" in msg:
                return {"error": "Email already exists"}, 409
            return {"error": msg}, 400

        return _public_user_dict(user), 201

    @users_api.response(200, "List of users", fields.List(fields.Nested(user_output)))
    def get(self):
        """List all users."""
        users = facade.list_users()
        return [_public_user_dict(u) for u in users], 200


@users_api.route("/<string:user_id>")
class UserItem(Resource):
    @users_api.response(200, "User found", user_output)
    @users_api.response(404, "User not found")
    def get(self, user_id):
        """Get one user by ID."""
        user = facade.get_user(user_id)
        if user is None:
            return {"error": "User not found"}, 404
        return _public_user_dict(user), 200

    @users_api.expect(user_update)
    @users_api.response(200, "User updated", user_output)
    @users_api.response(400, "Bad request")
    @users_api.response(404, "User not found")
    @users_api.response(409, "Email already exists")
    def put(self, user_id):
        """Update a user by ID."""
        data = request.get_json(silent=True) or {}

        try:
            user = facade.update_user(user_id, data)
        except KeyError:
            return {"error": "User not found"}, 404
        except ValueError as e:
            msg = str(e)
            if "must be unique" in msg:
                return {"error": "Email already exists"}, 409
            return {"error": msg}, 400

        return _public_user_dict(user), 200
