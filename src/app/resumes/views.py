from flask import Blueprint, abort, render_template
from flask_login import current_user

from app.dashboards.models import Profile

blueprint = Blueprint('resumes', __name__, url_prefix='/resume')


def show_resume(username: str):
    profile = Profile.query.filter_by(username=username).first_or_404()

    if not profile.resume.is_visible:
        if current_user.is_authenticated:
            if current_user.profile.id != profile.id:
                abort(404)
        else:
            abort(404)

    work_datas = profile.work_datas
    social = profile.social
    experience = profile.experience
    education = profile.education
    skill = profile.skill

    return render_template('resumes/resume.html', profile=profile, workdata=work_datas, social=social,
                           experiences=experience,
                           educations=education, skills=skill)


blueprint.add_url_rule('/<string:username>', view_func=show_resume, methods=["GET"])
