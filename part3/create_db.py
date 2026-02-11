from app.app import create_app
from app.extensions import db, bcrypt
from app.models.user import User

def seed_user():
    email = "test@example.com"
    password = "Test12345!"   # كلمة مرور معروفة
    first_name = "Test"
    last_name = "User"
    is_admin = True

    # إذا موجود لا تعيد إنشاءه
    existing = User.query.filter_by(email=email).first()
    if existing:
        print("User already exists ✅")
        print("EMAIL:", email)
        print("PASSWORD:", password)
        return

    # خزّنها كهاش (المفروض موديلك يسويها أو نسويها هنا)
    hashed = bcrypt.generate_password_hash(password).decode("utf-8")

    u = User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=hashed,      # أو password_hash حسب اسم العمود عندك
        is_admin=is_admin
    )

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

