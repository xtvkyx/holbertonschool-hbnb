from flask_restx import Namespace, Resource, fields
from hbnb.facade import get_facade

facade = get_facade()

places_ns = Namespace("places", description="Place operations")

# ---------- Nested output models ----------
owner_model = places_ns.model(
    "Owner",
    {
        "id": fields.String(required=True),
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
        "email": fields.String(required=True),
    },
)

amenity_model = places_ns.model(
    "Amenity",
    {
        "id": fields.String(required=True),
        "name": fields.String(required=True),
    },
)

# ---------- Output model ----------
place_model = places_ns.model(
    "Place",
    {
        "id": fields.String(readOnly=True),
        "title": fields.String(required=True),
        "description": fields.String(required=False),
        "price_per_night": fields.Float(required=True),
        "latitude": fields.Float(required=True),
        "longitude": fields.Float(required=True),
        "owner": fields.Nested(owner_model, required=True),
        "amenities": fields.List(fields.Nested(amenity_model)),
    },
)

# ---------- Input models ----------
place_create_model = places_ns.model(
    "PlaceCreate",
    {
        "owner_id": fields.String(required=True),
        "title": fields.String(required=True),
        "description": fields.String(required=False),
        "price_per_night": fields.Float(required=True),
        "latitude": fields.Float(required=True),
        "longitude": fields.Float(required=True),
        "amenity_ids": fields.List(fields.String, required=False),
    },
)

place_update_model = places_ns.model(
    "PlaceUpdate",
    {
        "title": fields.String(required=False),
        "description": fields.String(required=False),
        "price_per_night": fields.Float(required=False),
        "latitude": fields.Float(required=False),
        "longitude": fields.Float(required=False),
        "amenity_ids": fields.List(fields.String, required=False),
    },
)


@places_ns.route("")
class PlaceListResource(Resource):
    @places_ns.marshal_list_with(place_model)
    def get(self):
        return facade.get_places(), 200

    @places_ns.expect(place_create_model, validate=True)
    @places_ns.marshal_with(place_model, code=201)
    def post(self):
        data = places_ns.payload or {}
        try:
            return facade.create_place(data), 201
        except KeyError as e:
            places_ns.abort(404, str(e))
        except ValueError as e:
            places_ns.abort(400, str(e))


@places_ns.route("/<string:place_id>")
@places_ns.param("place_id", "Place identifier")
class PlaceResource(Resource):
    @places_ns.marshal_with(place_model)
    def get(self, place_id):
        place = facade.get_place(place_id)
        if place is None:
            places_ns.abort(404, "Place not found")
        return place, 200

    @places_ns.expect(place_update_model, validate=True)
    @places_ns.marshal_with(place_model)
    def put(self, place_id):
        data = places_ns.payload or {}
        existing = facade.get_place(place_id)
        if existing is None:
            places_ns.abort(404, "Place not found")

        try:
            updated = facade.update_place(place_id, data)
            if updated is None:
                places_ns.abort(404, "Place not found")
            return updated, 200
        except KeyError as e:
            places_ns.abort(404, str(e))
        except ValueError as e:
            places_ns.abort(400, str(e))
