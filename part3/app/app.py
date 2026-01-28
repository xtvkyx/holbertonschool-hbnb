from flask import Flask
from config import Config
from app.extensions import db, jwt, bcrypt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    from app.api.v1.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/v1")

    from app.api.v1.routes import blueprint as api_v1_blueprint
    app.register_blueprint(api_v1_blueprint)

    return app

