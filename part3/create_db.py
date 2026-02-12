from app.app import create_app
from app.extensions import db
from app.models.user import User

def seed_user():
    email = "test@example.com"
    password = "Test12345!"   # كلمة مرور معروفة
    is_admin = True

    # إذا موجود لا تعيد إنشاءه
    existing = User.query.filter_by(email=email).first()
    if existing:
        print("User already exists ✅")
        print("EMAIL:", email)
        print("PASSWORD:", password)
        return

    u = User(email=email, is_admin=is_admin)
    u.set_password(password)

    db.session.add(u)
    db.session.commit()

    print("Seed user created ✅")
    print("EMAIL:", email)
    print("PASSWORD:", password)

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
        seed_user()
        print("DB tables created ✅")

