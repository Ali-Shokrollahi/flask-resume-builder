from app.extensions import db
from app.utils.models import BaseModel
from app.resumes.models import Resume


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
    experience = db.relationship('Experience')
    education = db.relationship('Education')
    skill = db.relationship('Skill')

    resume = db.relationship('app.resumes.models.Resume', uselist=False)

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

    experience = db.Column(db.SMALLINT, nullable=False)
    number_of_projects = db.Column(db.SMALLINT, nullable=False)
    number_of_customer = db.Column(db.SMALLINT, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), unique=True)


class Experience(BaseModel):
    __tablename__ = "experiences"
    title = db.Column(db.String(64), nullable=False)
    company = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text())
    duration = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))


class Education(BaseModel):
    __tablename__ = "educations"
    title = db.Column(db.String(32), nullable=False)
    school = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text())
    duration = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))


class Skill(BaseModel):
    __tablename__ = "skills"

    name = db.Column(db.String(32), nullable=False)
    percent = db.Column(db.Integer, nullable=False, default=0)
    owner_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))
