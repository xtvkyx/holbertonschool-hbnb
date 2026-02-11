from flask import Flask
from flask_restx import Api

rest_api = Api(
    title="HBnB API",
    version="1.0",
    description="HBnB API"
)

def create_app(config_object="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    rest_api.init_app(app)

    from app.api.v1.routes import register_routes
    register_routes(rest_api)

    return app
