"""API v1 routes."""
from flask_restx import Namespace, Resource

api = Namespace("status", description="Health check endpoints")


@api.route("/health")
class Health(Resource):
    def get(self):
        return {"status": "ok"}, 200
