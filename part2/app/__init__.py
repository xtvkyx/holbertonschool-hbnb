from flask import Flask
from flask_restx import Api

api = Api(
    title="HBnB API",
    version="1.0",
    description="HBnB API v1"
)

def create_app(config_object="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    api.init_app(app)

    # Register v1 routes/namespaces
    from app.api.v1.routes import api_bp
    app.register_blueprint(api_bp)

    return app
