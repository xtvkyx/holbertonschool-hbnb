class Config:
    SECRET_KEY = "dev-secret-key"

    # Database (SQLite for development)
    SQLALCHEMY_DATABASE_URI = "sqlite:///hbnb.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # JWT
    JWT_SECRET_KEY = "jwt-secret-key"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
