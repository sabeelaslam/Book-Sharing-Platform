from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash
import getpass

admin_user = " "
def create_admin():
    app = create_app()
    with app.app_context():
        print("--- Create Admin User ---")
        username = input("Enter admin username: ")
        email = input("Enter admin email: ")
        password = input("Enter admin password: ")

        # Check if user already exists
        if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
            print("Error: User with that email or username already exists.")
            return

        hashed_password = generate_password_hash(password)

        admin_user = User(
            username=username, 
            email=email, 
            password=hashed_password, 
            role='Admin', 
            is_blocked=False
        )

        db.session.add(admin_user)
        db.session.commit()
        print(f"Success! Admin user '{username}' created successfully.")

if __name__ == "__main__":
    create_admin()