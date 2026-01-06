from flask_restx import Namespace, Resource, fields
from hbnb.facade.hbnb_facade import HBnBFacade


facade = HBnBFacade()

amenities_ns = Namespace("amenities", description="Amenity operations")

# ========= Output Model (Response) =========
amenity_model = amenities_ns.model(
    "Amenity",
    {
        "id": fields.String(readOnly=True, description="Amenity ID"),
        "name": fields.String(required=True, description="Amenity name"),
        # فعّلي هذا فقط إذا موديل Amenity عندك فيه description
        # "description": fields.String(required=False, description="Amenity description"),
    },
)

# ========= Input Model (POST) =========
amenity_create_model = amenities_ns.model(
    "AmenityCreate",
    {
        "name": fields.String(required=True, description="Amenity name"),
        # فعّلي هذا فقط إذا موديل Amenity عندك فيه description
        # "description": fields.String(required=False, description="Amenity description"),
    },
)

# ========= Input Model (PUT) =========
amenity_update_model = amenities_ns.model(
    "AmenityUpdate",
    {
        "name": fields.String(required=False, description="Amenity name"),
        # فعّلي هذا فقط إذا موديل Amenity عندك فيه description
        # "description": fields.String(required=False, description="Amenity description"),
    },
)


def amenity_to_dict(amenity):
    """Convert Amenity object to dict for API response."""
    if hasattr(amenity, "to_dict"):
        return amenity.to_dict()

    # Fallback (لو ما عندك to_dict)
    return {
        "id": getattr(amenity, "id", None),
        "name": getattr(amenity, "name", None),
        # "description": getattr(amenity, "description", None),
    }


@amenities_ns.route("")
class AmenityListResource(Resource):
    @amenities_ns.marshal_list_with(amenity_model)
    def get(self):
        """List all amenities"""
        amenities = facade.get_amenities()
        return [amenity_to_dict(a) for a in amenities], 200

    @amenities_ns.expect(amenity_create_model, validate=True)
    @amenities_ns.marshal_with(amenity_model, code=201)
    def post(self):
        """Create a new amenity"""
        data = amenities_ns.payload or {}

        name = data.get("name")
        # فعّلي هذا فقط إذا تستخدمين description
        # description = data.get("description")

        try:
            # إذا موديلك بدون description:
            amenity = facade.create_amenity(name=name)

            # إذا موديلك معه description، استخدمي هذا بدل اللي فوق:
            # amenity = facade.create_amenity(name=name, description=description)

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
        return amenity_to_dict(amenity), 200

    @amenities_ns.expect(amenity_update_model, validate=True)
    @amenities_ns.marshal_with(amenity_model)
    def put(self, amenity_id):
        """Update an existing amenity"""
        data = amenities_ns.payload or {}

        # خيار آمن: تأكدي موجود قبل التحديث
        existing = facade.get_amenity(amenity_id)
        if existing is None:
            amenities_ns.abort(404, "Amenity not found")

        try:
            updated = facade.update_amenity(amenity_id, data)
        except ValueError as e:
            amenities_ns.abort(400, str(e))

        if updated is None:
            amenities_ns.abort(404, "Amenity not found")

        return amenity_to_dict(updated), 200
