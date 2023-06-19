from app.extensions import db
from app.utils.models import BaseModel


class Profile(BaseModel):
    GENDER_CHOICES = [
        ("male", "مرد"),
        ("female", "زن"),
        ("other", "دیگر")
    ]
    username = db.Column(db.String(32), unique=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(30))
    job = db.Column(db.String(30))
    bio = db.Column(db.Text())
    gender = db.Column(db.String(5))
    birthday = db.Column(db.Date)
    photo = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)

    def __repr__(self):
        return self.user.email
