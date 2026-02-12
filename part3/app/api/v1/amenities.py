from flask import request
from flask_restx import Namespace, Resource, fields

from app.services.hbnb_facade import HBnBFacade

amenities_api = Namespace("amenities", description="Amenities operations")
facade = HBnBFacade()

amenity_model = amenities_api.model("Amenity", {
    "id": fields.String(readonly=True),
    "name": fields.String(required=True),
})

@amenities_api.route("/")
class AmenityList(Resource):
    @amenities_api.marshal_list_with(amenity_model)
    def get(self):
        return facade.get_amenities()

    @amenities_api.expect(amenity_model, validate=True)
    @amenities_api.marshal_with(amenity_model, code=201)
    def post(self):
        data = request.get_json() or {}
        amenity = facade.create_amenity(name=data.get("name"))
        return amenity, 201

@amenities_api.route("/<string:amenity_id>")
class AmenityItem(Resource):
    @amenities_api.marshal_with(amenity_model)
    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if amenity is None:
            amenities_api.abort(404, "Amenity not found")
        return amenity

    @amenities_api.expect(amenity_model, validate=True)
    @amenities_api.marshal_with(amenity_model)
    def put(self, amenity_id):
        data = request.get_json() or {}
        amenity = facade.update_amenity(amenity_id, name=data.get("name"))
        if amenity is None:
            amenities_api.abort(404, "Amenity not found")
        return amenity

    def delete(self, amenity_id):
        ok = facade.delete_amenity(amenity_id)
        if not ok:
            amenities_api.abort(404, "Amenity not found")
        return {"message": "Amenity deleted"}, 200
