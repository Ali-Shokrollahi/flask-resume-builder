from flask import Blueprint, abort, render_template, make_response
from flask_login import current_user, login_required
import pdfkit

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


    return render_template('resumes/resume.html', profile=profile)


def download_pdf(username: str):
    profile = Profile.query.filter_by(username=username).first_or_404()
    if not profile.resume.public_pdf_download:
        if current_user.is_authenticated:
            if current_user.profile.id != profile.id:
                abort(404)
        else:
            abort(404)

    html = render_template('resumes/test.html', profile=profile)
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    options = {
        "orientation": "portrait",
        "page-size": "A4",
        "margin-top": "0cm",
        "margin-right": "0cm",
        "margin-bottom": "0cm",
        "margin-left": "0cm",
        "encoding": "UTF-8",
        "enable-local-file-access": ""

    }

    pdf = pdfkit.from_string(html, options=options, configuration=config)

    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=output.pdf"
    return response


blueprint.add_url_rule('/<string:username>', view_func=show_resume, methods=["GET"])
blueprint.add_url_rule('/pdf-download/<string:username>', view_func=download_pdf, methods=["GET"])
