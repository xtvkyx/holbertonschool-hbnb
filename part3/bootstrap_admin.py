from hbnb.app import create_app
from hbnb.extensions import db
from hbnb.models.user import User


def main():
    app = create_app()
    with app.app_context():
        email = "admin@example.com"
        password = "Admin123!"

        existing = User.query.filter_by(email=email).first()
        if existing:
            print("Admin already exists ✅")
            return

        admin = User(email=email, is_admin=True, first_name="Admin", last_name="User")
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print("Admin created ✅", email, password)


if __name__ == "__main__":
    main()
