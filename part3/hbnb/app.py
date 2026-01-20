from flask import Flask
from hbnb.extensions import bcrypt
from hbnb.api.v1.routes import blueprint as api_v1_blueprint


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bcrypt.init_app(app)

    #just register blueprint (it already has the Api + namespaces)
    app.register_blueprint(api_v1_blueprint)

    return app
