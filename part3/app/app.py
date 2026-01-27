from flask import Flask
from app.config import Config
from app.extensions import db, jwt, bcrypt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    from app.api.v1.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/v1")

    return app
