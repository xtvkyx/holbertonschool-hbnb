from flask import request
from flask_restx import Namespace, Resource, fields

from hbnb.models import User

users_api = Namespace("users", description="User endpoints")

# simple in-memory storage for Task 1
_USERS = {}
_NEXT_ID = 1


user_create = users_api.model("UserCreate", {
    "first_name": fields.String(required=True),
    "last_name": fields.String(required=True),
    "email": fields.String(required=True),
    "password": fields.String(required=True),
    "is_admin": fields.Boolean(required=False),
})

user_out = users_api.model("UserOut", {
    "id": fields.Integer,
    "first_name": fields.String,
    "last_name": fields.String,
    "email": fields.String,
    "is_admin": fields.Boolean,
})


@users_api.route("/")
class UsersCollection(Resource):
    @users_api.expect(user_create)
    @users_api.response(201, "User created", user_out)
    @users_api.response(400, "Bad request")
    @users_api.response(409, "Email already exists")
    def post(self):
        global _NEXT_ID
        data = request.get_json(silent=True) or {}

        # enforce unique email (simple in-memory check)
        email = (data.get("email") or "").strip().lower()
        if any(u.email == email for u in _USERS.values()):
            return {"error": "Email already exists"}, 409

        try:
            user = User(
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                email=data.get("email"),
                password=data.get("password"),
                is_admin=data.get("is_admin", False),
            )
        except ValueError as e:
            return {"error": str(e)}, 400

        user.id = _NEXT_ID
        _USERS[_NEXT_ID] = user
        _NEXT_ID += 1

        # ✅ do NOT return password or hash
        return user.to_public_dict(), 201
