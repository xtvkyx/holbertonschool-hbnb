from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from app.services.hbnb_facade import HBnBFacade

places_api = Namespace("places", description="Places operations")
facade = HBnBFacade()

place_model = places_api.model("Place", {
    "id": fields.String(readonly=True),
    "title": fields.String(required=True),
    "description": fields.String,
    "price": fields.Float,
    "latitude": fields.Float,
    "longitude": fields.Float,
    "owner_id": fields.String,
})

@places_api.route("/")
class PlaceList(Resource):

    @places_api.marshal_list_with(place_model)
    def get(self):
        return facade.list_places()

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

