from flask import request
from flask_restx import Namespace, Resource, fields
from app.extensions import db
from app.models.user import User

users_api = Namespace("users", description="User endpoints")

user_create = users_api.model("UserCreate", {
    "email": fields.String(required=True),
    "password": fields.String(required=True),
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
        data = request.get_json()

        email = data["email"].lower()
        password = data["password"]

        if User.query.filter_by(email=email).first():
            users_api.abort(409, "Email exists")

        user = User(email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return user, 201

