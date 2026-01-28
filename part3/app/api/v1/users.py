from flask import request
from flask_restx import Namespace, Resource, fields

from app.extensions import db
from app.models.user import User

users_api = Namespace("users", description="User endpoints")

user_create = users_api.model("UserCreate", {
    "email": fields.String(required=True),
    "password": fields.String(required=True),
    "is_admin": fields.Boolean(required=False, default=False),
})

user_out = users_api.model("UserOut", {
    "id": fields.String,
    "email": fields.String,
    "is_admin": fields.Boolean,
})

@users_api.route("/")
class UsersCollection(Resource):
    @users_api.expect(user_create, validate=True)
    @users_api.marshal_with(user_out, code=201)
    def post(self):
        data = request.get_json() or {}
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""

        # Basic validation
        if not email or not password:
            users_api.abort(400, "email and password are required")

        # Unique email check
        if User.query.filter_by(email=email).first() is not None:
            users_api.abort(409, "Email already exists")

        user = User(email=email, is_admin=bool(data.get("is_admin", False)))
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return user, 201
