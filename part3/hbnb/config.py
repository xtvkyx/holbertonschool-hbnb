class Config:
    SECRET_KEY = "dev-secret-key"

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
