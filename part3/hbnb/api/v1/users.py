from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from hbnb.extensions import db
from hbnb.models.user import User

users_bp = Blueprint("users", __name__)

@users_bp.get("/users/<user_id>")
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"error": "not found"}, 404
    return user.to_dict(), 200

@users_bp.put("/users/me")
@jwt_required()
def update_me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return {"error": "not found"}, 404

    data = request.get_json() or {}

    # ممنوع تعديلها
    for k in ("email", "password", "password_hash", "is_admin", "id"):
        data.pop(k, None)

    # عدلي هنا حسب حقول User عندك
    if "first_name" in data:
        user.first_name = data["first_name"]
    if "last_name" in data:
        user.last_name = data["last_name"]

    db.session.commit()
    return user.to_dict(), 200
