from app import create_app
from models import db, User

app = create_app()

NEW_EMAIL = "mdsalikamir@gmail.com"
NEW_PASSWORD = "Salik@#786"

with app.app_context():

    admin = User.query.filter_by(role='admin').first()

    if admin:
        admin.email = NEW_EMAIL
        admin.set_password(NEW_PASSWORD)

        db.session.commit()

        print("================================")
        print("Admin details updated!")
        print("Email:", NEW_EMAIL)
        print("Password:", NEW_PASSWORD)
        print("================================")

    else:
        print("Admin user not found!")