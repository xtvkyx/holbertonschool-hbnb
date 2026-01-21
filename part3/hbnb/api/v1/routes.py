from flask import Blueprint

api_v1 = Blueprint("api_v1", __name__)

# Import and register sub-blueprints
from hbnb.api.v1.auth import auth_bp
from hbnb.api.v1.users import users_bp
from hbnb.api.v1.places import places_bp
from hbnb.api.v1.reviews import reviews_bp

api_v1.register_blueprint(auth_bp)
api_v1.register_blueprint(users_bp)
api_v1.register_blueprint(places_bp)
api_v1.register_blueprint(reviews_bp)
