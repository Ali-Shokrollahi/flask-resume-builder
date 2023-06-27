import getpass
from flask.cli import AppGroup

from app.dashboards.models import Profile
from app.extensions import db
from app.accounts.models import User
from app.resumes.models import Resume

admin_cli = AppGroup('admin', help='Admin commands.')


@admin_cli.command('create')
def create_admin():
    """Creates the admin user."""
    email = input("Enter email address: ")
    password = getpass.getpass("Enter password: ")
    confirm_password = getpass.getpass("Enter password again: ")
    if password != confirm_password:
        print("Passwords don't match")
        return 1
    try:
        user = User(email=email, is_admin=True, is_active=True, email_verified=True)
        user.set_user_password(password)
        db.session.add(user)
        db.session.flush()
        profile = Profile(user_id=user.id)
        resume = Resume(owner_id=user.id)
        db.session.add(profile)
        db.session.add(resume)
        db.session.commit()
        print(f"Admin with email {email} created successfully!")
    except Exception:
        print("Couldn't create admin user.")
