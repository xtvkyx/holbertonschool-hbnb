from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from hbnb.extensions import db, bcrypt
from hbnb.models.user import User
from hbnb.api.v1.admin_utils import admin_required

users_bp = Blueprint("users", __name__)


# ------------------------
# Public: get user by id
# ------------------------
@users_bp.get("/users/<user_id>")
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"error": "not found"}, 404
    return user.to_dict(), 200


# ------------------------
# Authenticated user: update own profile
# (NO email / password / is_admin)
# ------------------------
@users_bp.put("/users/me")
@jwt_required()
def update_me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return {"error": "not found"}, 404

    data = request.get_json() or {}

    # forbidden fields for regular users
    for k in ("email", "password", "password_hash", "is_admin", "id"):
        data.pop(k, None)

    # update allowed fields (adjust if your User model differs)
    if "first_name" in data:
        user.first_name = data["first_name"]
    if "last_name" in data:
        user.last_name = data["last_name"]

    db.session.commit()
    return user.to_dict(), 200


# ------------------------
# Admin: create user
# ------------------------
@users_bp.post("/users")
@admin_required()
def create_user():
    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {"error": "email and password required"}, 400

    # unique email check
    if User.query.filter_by(email=email).first():
        return {"error": "email already exists"}, 400

    user = User(
        email=email,
        is_admin=data.get("is_admin", False)
    )
    user.set_password(password)

    # optional fields
    if "first_name" in data:
        user.first_name = data["first_name"]
    if "last_name" in data:
        user.last_name = data["last_name"]

    db.session.add(user)
    db.session.commit()
    return user.to_dict(), 201


# ------------------------
# Admin: update any user
# (including email + password)
# ------------------------
@users_bp.put("/users/<user_id>")
@admin_required()
def admin_update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"error": "not found"}, 404

    data = request.get_json() or {}

    # update email (with uniqueness check)
    if "email" in data:
        existing = User.query.filter(
            User.email == data["email"],
            User.id != user_id
        ).first()
        if existing:
            return {"error": "email already exists"}, 400
        user.email = data["email"]

    # update password
    if "password" in data:
        user.set_password(data["password"])

    # update admin flag
    if "is_admin" in data:
        user.is_admin = bool(data["is_admin"])

    # optional fields
    if "first_name" in data:
        user.first_name = data["first_name"]
    if "last_name" in data:
        user.last_name = data["last_name"]

    db.session.commit()
    return user.to_dict(), 200
