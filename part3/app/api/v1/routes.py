from flask import Blueprint
from flask_restx import Api

from app.api.v1.users import users_api
from app.api.v1.places import places_api
from app.api.v1.reviews import reviews_api
from app.api.v1.amenities import amenities_api

blueprint = Blueprint("api_v1", __name__, url_prefix="/api/v1")
api = Api(blueprint)

api.add_namespace(users_api, path="/users")
api.add_namespace(places_api, path="/places")
api.add_namespace(reviews_api, path="/reviews")
api.add_namespace(amenities_api, path="/amenities")

