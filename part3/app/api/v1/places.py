from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from app.services.hbnb_facade import HBnBFacade

places_api = Namespace("places", description="Places operations")
facade = HBnBFacade()

amenity_model = places_api.model("Amenity", {
    "id": fields.String(readonly=True),
    "name": fields.String,
})

review_model = places_api.model("Review", {
    "id": fields.String(readonly=True),
    "text": fields.String,
    "rating": fields.Integer,
    "user_id": fields.String,
    "place_id": fields.String,
})

place_model = places_api.model("Place", {
    "id": fields.String(readonly=True),
    "title": fields.String(required=True),
    "description": fields.String,
    "price": fields.Float,
    "latitude": fields.Float,
    "longitude": fields.Float,
    "owner_id": fields.String,
    "amenities": fields.List(fields.Nested(amenity_model)),
    "reviews": fields.List(fields.Nested(review_model)),
})

@places_api.route("/")
class PlaceList(Resource):

    @places_api.marshal_list_with(place_model)
    def get(self):
        return facade.get_places()

    @jwt_required()  # ✅ MUST be first
    @places_api.expect(place_model, validate=True)
    @places_api.marshal_with(place_model, code=201)
    def post(self):
        data = request.get_json() or {}

        place = facade.create_place(
            title=data.get("title"),
            description=data.get("description"),
            price=data.get("price", 0.0),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            owner_id=data.get("owner_id"),
        )

        return place, 201


@places_api.route("/<string:place_id>")
class PlaceItem(Resource):

    @places_api.marshal_with(place_model)
    def get(self, place_id):
        place = facade.get_place(place_id)
        if place is None:
            places_api.abort(404, "Place not found")

        data = place.to_dict() if hasattr(place, "to_dict") else {}
        data.setdefault("latitude", getattr(place, "latitude", None))
        data.setdefault("longitude", getattr(place, "longitude", None))

        amenities = getattr(place, "amenities", []) or []
        reviews = getattr(place, "reviews", []) or []

        data["amenities"] = [a.to_dict() if hasattr(a, "to_dict") else {"id": getattr(a, "id", None), "name": getattr(a, "name", None)} for a in amenities]
        data["reviews"] = [r.to_dict() if hasattr(r, "to_dict") else {"id": getattr(r, "id", None), "text": getattr(r, "text", None), "rating": getattr(r, "rating", None), "user_id": getattr(r, "user_id", None), "place_id": getattr(r, "place_id", None)} for r in reviews]

        return data

