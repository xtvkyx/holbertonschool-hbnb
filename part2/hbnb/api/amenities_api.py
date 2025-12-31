from flask_restx import Namespace, Resource, fields
from hbnb.facade.hbnb_facade import HBnBFacade  # adjust if you have get_facade()


# If you have a get_facade() function in facade/__init__.py, use that instead:
# from hbnb.facade import get_facade
# facade = get_facade()
facade = HBnBFacade()

amenities_ns = Namespace("amenities", description="Amenity operations")

# Model used for input/output
amenity_model = amenities_ns.model("Amenity", {
    "id": fields.String(readonly=True, description="Amenity ID"),
    "name": fields.String(required=True, description="Amenity name"),
    "description": fields.String(required=False, description="Amenity description"),
})


def amenity_to_dict(amenity):
    """Helper to convert Amenity object into a dict for the API."""
    if hasattr(amenity, "to_dict"):
        return amenity.to_dict()

    # Fallback if you don’t have to_dict()
    return {
        "id": getattr(amenity, "id", None),
        "name": getattr(amenity, "name", None),
        "description": getattr(amenity, "description", None),
    }


@amenities_ns.route("")
class AmenityListResource(Resource):
    @amenities_ns.marshal_list_with(amenity_model)
    def get(self):
        """List all amenities"""
        amenities = facade.get_amenities()
        return [amenity_to_dict(a) for a in amenities]

    @amenities_ns.expect(amenity_model, validate=True)
    @amenities_ns.marshal_with(amenity_model, code=201)
    def post(self):
        """Create a new amenity"""
        data = amenities_ns.payload or {}
        name = data.get("name")
        description = data.get("description")

        try:
            amenity = facade.create_amenity(name=name, description=description)
        except ValueError as e:
            amenities_ns.abort(400, str(e))

        return amenity_to_dict(amenity), 201


@amenities_ns.route("/<string:amenity_id>")
@amenities_ns.param("amenity_id", "The amenity identifier")
class AmenityResource(Resource):
    @amenities_ns.marshal_with(amenity_model)
    def get(self, amenity_id):
        """Get a single amenity by ID"""
        amenity = facade.get_amenity(amenity_id)
        if amenity is None:
            amenities_ns.abort(404, "Amenity not found")
        return amenity_to_dict(amenity)

    @amenities_ns.expect(amenity_model, validate=False)
    @amenities_ns.marshal_with(amenity_model)
    def put(self, amenity_id):
        """Update an existing amenity"""
        data = amenities_ns.payload or {}
        amenity = facade.update_amenity(amenity_id, data)
        if amenity is None:
            amenities_ns.abort(404, "Amenity not found")
        return amenity_to_dict(amenity)

    # ❌ No DELETE here on purpose (task says no delete for amenities)

