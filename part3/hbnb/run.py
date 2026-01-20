from hbnb.app import create_app
from hbnb.config import DevelopmentConfig

app = create_app(DevelopmentConfig)

if __name__ == "__main__":
    app.run()
