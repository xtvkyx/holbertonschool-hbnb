from hbnb.app import create_app
from hbnb.extensions import db
from hbnb.models import User  # ensures models are imported/mapped


def main():
    app = create_app()
    with app.app_context():
        db.create_all()
        print("DB tables created ✅")


if __name__ == "__main__":
    main()
