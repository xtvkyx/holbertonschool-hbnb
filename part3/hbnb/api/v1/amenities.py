from flask import Blueprint, request
from hbnb.api.v1.admin_utils import admin_required
from hbnb.extensions import db
from hbnb.models.amenity import Amenity

amenities_bp = Blueprint("amenities", __name__)

@amenities_bp.get("/amenities")
def list_amenities():
    amenities = Amenity.query.all()
    return [a.to_dict() for a in amenities], 200

@amenities_bp.post("/amenities")
@admin_required()
def create_amenity():
    data = request.get_json() or {}
    name = data.get("name")

    if not name:
        return {"error": "name required"}, 400

    if Amenity.query.filter_by(name=name).first():
        return {"error": "amenity already exists"}, 400

    a = Amenity(name=name)
    db.session.add(a)
    db.session.commit()
    return a.to_dict(), 201

@amenities_bp.put("/amenities/<amenity_id>")
@admin_required()
def update_amenity(amenity_id):
    a = Amenity.query.get(amenity_id)
    if not a:
        return {"error": "not found"}, 404

    data = request.get_json() or {}
    if "name" in data:
        new_name = data["name"]
        existing = Amenity.query.filter(Amenity.name == new_name, Amenity.id != amenity_id).first()
        if existing:
            return {"error": "amenity already exists"}, 400
        a.name = new_name

    db.session.commit()
    return a.to_dict(), 200
