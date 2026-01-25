from flask_restx import Namespace, Resource, fields
from hbnb.facade import get_facade

facade = get_facade()

places_ns = Namespace("places", description="Place operations")

# =====================================================
# Models
# =====================================================

amenity_out_model = places_ns.model(
    "AmenityOut",
    {
        "id": fields.String(required=True),
        "name": fields.String(required=True),
    },
)

review_out_model = places_ns.model(
    "PlaceReview",
    {
        "id": fields.String(required=True),
        "user_id": fields.String(required=True),
        "place_id": fields.String(required=True),
        "rating": fields.Integer(required=True),
        "comment": fields.String(required=True),
    },
)

place_model = places_ns.model(
    "Place",
    {
        "id": fields.String(readOnly=True),
        "title": fields.String(required=True),
        "description": fields.String,
        "price_per_night": fields.Float(required=True),
        "latitude": fields.Float(required=True),
        "longitude": fields.Float(required=True),
        "owner": fields.Raw,  # dict with id, first_name, last_name, email
        "amenities": fields.List(fields.Nested(amenity_out_model)),
        "reviews": fields.List(fields.Nested(review_out_model)),
    },
)

place_create_model = places_ns.model(
    "PlaceCreate",
    {
        "owner_id": fields.String(required=True),
        "title": fields.String(required=True),
        "description": fields.String,
        "price_per_night": fields.Float(required=True),
        "latitude": fields.Float(required=True),
        "longitude": fields.Float(required=True),
        "amenity_ids": fields.List(fields.String),
    },
)

place_update_model = places_ns.model(
    "PlaceUpdate",
    {
        "title": fields.String,
        "description": fields.String,
        "price_per_night": fields.Float,
        "latitude": fields.Float,
        "longitude": fields.Float,
        "amenity_ids": fields.List(fields.String),
    },
)

# =====================================================
# Routes
# =====================================================

@places_ns.route("")
class PlaceListResource(Resource):
    @places_ns.marshal_list_with(place_model)
    def get(self):
        """List all places"""
        return facade.get_places(), 200

    @places_ns.expect(place_create_model, validate=True)
    @places_ns.marshal_with(place_model, code=201)
    def post(self):
        """Create a new place"""
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
        try:
            updated = facade.update_place(place_id, places_ns.payload or {})
            if updated is None:
                places_ns.abort(404, "Place not found")
            return updated, 200
        except ValueError as e:
            places_ns.abort(400, str(e))


@places_ns.route("/<string:place_id>/reviews")
@places_ns.param("place_id", "Place identifier")
class PlaceReviewsResource(Resource):
    @places_ns.marshal_list_with(review_out_model)
    def get(self, place_id):
        """Get all reviews for a place"""
        try:
            return facade.get_place_reviews(place_id), 200
        except KeyError as e:
            places_ns.abort(404, str(e))
