from flask import Flask
from app.extensions import db, jwt, bcrypt
from app.api.v1.routes import blueprint as api_v1_blueprint

def create_app(config_name="default"):
    app = Flask(__name__)

    # BASIC CONFIG (for tests)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "test-secret"

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.models.place_amenity import place_amenity 
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

    with app.app_context():
        db.create_all()

    return app

