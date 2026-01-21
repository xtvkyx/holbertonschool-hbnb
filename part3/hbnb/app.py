from flask import Flask
from hbnb.config import Config
from hbnb.extensions import db, jwt, bcrypt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    from hbnb.api.v1.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/v1")

    return app
