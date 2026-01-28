from flask import Blueprint
from flask_restx import Api

from app.api.v1.users import users_api

blueprint = Blueprint("api_v1", __name__, url_prefix="/api/v1")

api = Api(
    blueprint,
    title="HBnB API",
    version="1.0",
    description="HBnB API v1"
)

#Api has add_namespace()
api.add_namespace(users_api, path="/users")
