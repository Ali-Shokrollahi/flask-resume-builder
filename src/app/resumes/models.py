from app.utils.models import BaseModel
from app.extensions import db


class Resume(BaseModel):
    __tablename__ = "resumes"

    owner_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), unique=True)
    is_allowed = db.Column(db.Boolean, nullable=False, default=False)
    is_visible = db.Column(db.Boolean, nullable=False, default=False)
    public_pdf_download = db.Column(db.Boolean, nullable=False, default=False)
