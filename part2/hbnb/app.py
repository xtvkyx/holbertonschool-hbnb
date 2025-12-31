"""Flask application factory."""
from flask import Flask
from flask_restx import Api
from hbnb.api.v1.routes import blueprint as api_v1_blueprint
from hbnb.api.v1.routes import api as v1_api


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(api_v1_blueprint)
    api = Api(
        app,
        title="HBnB API",
        version="1.0",
        description="HBnB Evolution - Part 2"
    )

    api.add_namespace(v1_api, path="/api/v1")
    return app
