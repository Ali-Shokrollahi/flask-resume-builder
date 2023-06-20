from app.extensions import db
from app.utils.models import BaseModel


class Profile(BaseModel):
    __tablename__ = "profiles"

    username = db.Column(db.String(32), unique=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(30))
    job = db.Column(db.String(30))
    bio = db.Column(db.Text())
    gender = db.Column(db.String(5))
    birthday = db.Column(db.Date)
    photo = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)

    social = db.relationship('Social', uselist=False)
    work_datas = db.relationship('WorkData', uselist=False)

    def __repr__(self):
        return self.user.email


class Social(BaseModel):
    __tablename__ = "socials"
    instagram = db.Column(db.String(32))
    telegram = db.Column(db.String(32))
    linkedin = db.Column(db.String(32))
    github = db.Column(db.String(32))
    pinterest = db.Column(db.String(32))
    address = db.Column(db.Text())
    owner_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), unique=True)

    def __repr__(self):
        return self.owner.email


class WorkData(BaseModel):
    __tablename__ = "work_datas"

    experience = db.Column(db.Integer, nullable=False)
    number_of_projects = db.Column(db.Integer, nullable=False)
    number_of_customer = db.Column(db.Integer, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), unique=True)
