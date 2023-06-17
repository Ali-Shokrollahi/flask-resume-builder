from app.extensions import db, bcrypt
from app.utils.models import BaseModel


class User(BaseModel):
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    email_verified = db.Column(db.Boolean, nullable=False, default=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return {self.email}

    def set_user_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_user_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
