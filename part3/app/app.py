from flask import Flask
from app.extensions import db, jwt, bcrypt
from app.api.v1.routes import blueprint as api_v1_blueprint
from config import config as config_map

def create_app(config_name="default"):
    app = Flask(__name__)

    cfg = config_map.get(config_name, config_map["default"])
    app.config.from_object(cfg)

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    from app.models.user import User
    from app.models.place import Place
    from app.models.review import Review
    from app.models.amenity import Amenity
    from app.models.associations import place_amenity

    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        return response

    # ✅ FORCE JWT ERRORS TO RETURN 401
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {"error": "Missing Authorization Header"}, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {"error": "Invalid token"}, 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {"error": "Token expired"}, 401

    app.register_blueprint(api_v1_blueprint)

    from app.api.v1.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/v1")

    with app.app_context():
        db.create_all()

    return app

