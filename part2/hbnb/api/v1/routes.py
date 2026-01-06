"""API v1 routes."""
from flask import Blueprint
from flask_restx import Api

from hbnb.api.v1.users import users_api
from hbnb.api.amenities_api import amenities_ns
from hbnb.api.places_api import places_ns
from hbnb.api.reviews_api import reviews_ns

blueprint = Blueprint("api_v1", __name__, url_prefix="/api/v1")
api = Api(blueprint, title="HBnB API", version="1.0", description="HBnB API v1")

# Namespaces
api.add_namespace(users_api, path="/users")
api.add_namespace(amenities_ns, path="/amenities")
api.add_namespace(places_ns, path="/places")
api.add_namespace(reviews_ns, path="/reviews")
