from flask_restx import Namespace, Resource, fields

ns = Namespace("amenities", description="Amenity operations")

amenity_model = ns.model("Amenity", {
    "id": fields.String(readonly=True),
    "name": fields.String(required=True, max_length=50),
})

@ns.route("/")
class AmenityList(Resource):
    @ns.marshal_list_with(amenity_model)
    def get(self):
        """List amenities"""
        return [], 200

    @ns.expect(amenity_model, validate=True)
    @ns.marshal_with(amenity_model, code=201)
    def post(self):
        """Create an amenity"""
        payload = ns.payload
        # Minimal stub to satisfy Swagger for now
        return {"id": "dummy-id", "name": payload.get("name")}, 201
