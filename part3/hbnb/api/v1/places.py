from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from hbnb.extensions import db
from hbnb.models.place import Place  # لازم يكون موجود عندك

places_bp = Blueprint("places", __name__)

@places_bp.get("/places")
def list_places():
    places = Place.query.all()
    return [p.to_dict() for p in places], 200

@places_bp.get("/places/<place_id>")
def get_place(place_id):
    place = Place.query.get(place_id)
    if not place:
        return {"error": "not found"}, 404
    return place.to_dict(), 200

@places_bp.post("/places")
@jwt_required()
def create_place():
    data = request.get_json() or {}
    user_id = get_jwt_identity()

    name = data.get("name")
    if not name:
        return {"error": "name required"}, 400

    place = Place(name=name, owner_id=user_id)
    db.session.add(place)
    db.session.commit()
    return place.to_dict(), 201

@places_bp.put("/places/<place_id>")
@jwt_required()
def update_place(place_id):
    user_id = get_jwt_identity()
    place = Place.query.get(place_id)
    if not place:
        return {"error": "not found"}, 404

    if place.owner_id != user_id:
        return {"error": "forbidden"}, 403

    data = request.get_json() or {}
    data.pop("owner_id", None)

    if "name" in data:
        place.name = data["name"]

    db.session.commit()
    return place.to_dict(), 200

@places_bp.delete("/places/<place_id>")
@jwt_required()
def delete_place(place_id):
    user_id = get_jwt_identity()
    place = Place.query.get(place_id)
    if not place:
        return {"error": "not found"}, 404

    if place.owner_id != user_id:
        return {"error": "forbidden"}, 403

    db.session.delete(place)
    db.session.commit()
    return {"message": "deleted"}, 200
