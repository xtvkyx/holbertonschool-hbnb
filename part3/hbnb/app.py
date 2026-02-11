from flask import Flask
from hbnb.config import Config
from hbnb.extensions import db, jwt, bcrypt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Register API v1 routes
    from hbnb.api.v1.routes import api_v1
    app.register_blueprint(api_v1, url_prefix="/api/v1")

    return app
