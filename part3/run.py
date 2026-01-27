from app.app import create_app
from config import DevelopmentConfig

app = create_app()

if __name__ == "__main__":
    app.run()
