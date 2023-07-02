from app.utils.models import BaseModel
from app.extensions import db


class Resume(BaseModel):
    __tablename__ = "resumes"

    owner_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), unique=True)
    is_allowed = db.Column(db.Boolean, nullable=False, default=False)
    is_visible = db.Column(db.Boolean, nullable=False, default=False)
    completion_percentage = db.Column(db.SMALLINT, nullable=False, default=0)
