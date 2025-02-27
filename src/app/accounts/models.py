from flask_login import UserMixin

from app.extensions import db, bcrypt
from app.utils.models import BaseModel
from sqlalchemy_utils import EmailType
from app.dashboards.models import Profile


class User(BaseModel, UserMixin):
    __tablename__ = "users"

    email = db.Column(EmailType, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    email_verified = db.Column(db.Boolean, nullable=False, default=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    profile = db.relationship('app.dashboards.models.Profile', backref='user', uselist=False)

    def __repr__(self):
        return self.email

    def set_user_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_user_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
