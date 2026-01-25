from flask import Blueprint
from flask_restx import Api

api_bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")
api = Api(api_bp, title="HBnB API", version="1.0", description="HBnB API v1")

from app.api.v1.users import ns as users_ns
api.add_namespace(users_ns, path="/users")
