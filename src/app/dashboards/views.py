import os

from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify, current_app, abort
from flask.views import MethodView
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from .forms import ProfileForm, SocialForm, WorkDataForm, ExperienceForm, EducationForm, SkillForm, \
    ResumeVisibilityForm, PortfolioForm
from app.extensions import db
from datetime import datetime

from .models import Profile, Social, WorkData, Experience, Education, Skill, Portfolio

blueprint = Blueprint('dashboards', __name__, url_prefix='/dashboard')


class ProfileUpdate(MethodView):
    decorators = [login_required]
    page = f"dashboards/forms/profile_update.html"

    def get(self):
        profile = current_user.profile
        form = ProfileForm()
        form.first_name.data = profile.first_name
        form.last_name.data = profile.last_name
        form.birthday.data = profile.birthday
        form.job.data = profile.job
        form.bio.data = profile.bio
        form.gender.data = profile.gender
        form.username.data = profile.username
        return render_template('dashboards/dashboard.html', page=self.page, form=form)

    def post(self):
        form = ProfileForm()
        profile = current_user.profile
        if form.validate_on_submit():
            profile.first_name = form.first_name.data
            profile.last_name = form.last_name.data
            if form.birthday.data:
                profile.birthday = datetime.strptime(form.birthday.data, '%Y-%m-%d')
            profile.job = form.job.data
            profile.bio = form.bio.data
            profile.gender = form.gender.data
            profile.username = form.username.data
            photo = form.photo.data

            if photo:
                filename = secure_filename(photo.filename)
                photo.save(os.path.join(current_app.config['UPLOAD_FOLDER'], 'profiles', filename))
                profile.photo = filename

            try:
                db.session.commit()
                flash('پروفایل با موفقیت تفییر یافت.', 'success')
                return redirect(url_for('dashboards.profile_update'))
            except:
                flash('خطایی در هنگام انجام عملیات رخ داده است. لطفا مجددا امتحان کنید.', category='danger')

        return render_template('dashboards/dashboard.html', page=self.page, form=form)


class SocialUpdate(MethodView):
    decorators = [login_required]

    page = f"dashboards/forms/social_update.html"

    def get(self):
        owner = current_user.profile
        socials = Social.query.filter_by(owner_id=owner.id).first()
        form = SocialForm()
        if socials:
            form.instagram.data = socials.instagram
            form.telegram.data = socials.telegram
            form.linkedin.data = socials.linkedin
            form.github.data = socials.github
            form.pinterest.data = socials.pinterest
            form.address.data = socials.address

        return render_template('dashboards/dashboard.html', page=self.page, form=form)

    def post(self):
        form = SocialForm()
        owner = current_user.profile
        socials = Social.query.filter_by(owner_id=owner.id).first()
        if form.validate_on_submit():

            if socials:
                socials.instagram = form.instagram.data
                socials.telegram = form.telegram.data
                socials.linkedin = form.linkedin.data
                socials.github = form.github.data
                socials.pinterest = form.pinterest.data
                socials.address = form.address.data

            else:
                so = Social(instagram=form.instagram.data, telegram=form.telegram.data,
                            linkedin=form.linkedin.data, github=form.github.data,
                            pinterest=form.pinterest.data, address=form.address.data, owner_id=owner.id)
                db.session.add(so)
            try:
                db.session.commit()
                flash('لینک های اجتماعی با موفقیت تفییر یافت.', 'success')
                return redirect(url_for('dashboards.social_update'))
            except:
                flash('خطایی در هنگام انجام عملیات رخ داده است. لطفا مجددا امتحان کنید.', category='danger')

        return render_template('dashboards/dashboard.html', page=self.page, form=form)


class WorkDataView(MethodView):
    decorators = [login_required]
    page = f"dashboards/forms/experience.html"

    def get(self):
        owner = current_user.profile
        work_data_form = WorkDataForm()
        experience_form = ExperienceForm()
        work_data = WorkData.query.filter_by(owner_id=owner.id).first()

        experiences = owner.experience
        if work_data:
            work_data_form.experience.data = work_data.experience
            work_data_form.number_of_projects.data = work_data.number_of_projects
            work_data_form.number_of_customer.data = work_data.number_of_customer

        return render_template('dashboards/dashboard.html', page=self.page, experiences=experiences,
                               experience_form=experience_form, work_data_form=work_data_form,
                               )

    def post(self):
        owner = current_user.profile
        form_id = request.args.get('form_id', 0, type=int)
        work_data_form = WorkDataForm()
        experience_form = ExperienceForm()

        if experience_form.validate_on_submit() and form_id == 2:
            ex = Experience(title=experience_form.title.data, company=experience_form.company.data,
                            description=experience_form.description.data, duration=experience_form.duration.data,
                            owner_id=owner.id)
            try:
                db.session.add(ex)
                db.session.commit()
                flash("اطلاعات با موفقیت ثبت شد.", 'success')

            except:
                flash("مشکلی پیش آمده است", 'danger')

        elif work_data_form.validate_on_submit() and form_id == 1:
            work_data = WorkData.query.filter_by(owner_id=owner.id).first()
            if work_data:
                work_data.experience = work_data_form.experience.data
                work_data.number_of_projects = work_data_form.number_of_projects.data
                work_data.number_of_customer = work_data_form.number_of_customer.data

            else:
                work_data = WorkData(experience=work_data_form.experience.data,
                                     number_of_projects=work_data_form.number_of_projects.data,
                                     number_of_customer=work_data_form.number_of_customer.data, owner_id=owner.id)
                db.session.add(work_data)

            try:

                db.session.commit()
                flash("اطلاعات با موفقیت ثبت شد.", 'success')
            except:
                flash("مشکلی پیش آمده است", 'danger')

        return redirect(url_for('dashboards.experiences'))


@login_required
def delete_exp():
    experience_id = request.form.get('id')
    exp = Experience.query.get_or_404(experience_id)
    if exp.owner_id == current_user.id:
        db.session.delete(exp)
        db.session.commit()
        return jsonify({'message': 'Experience deleted successfully'})
    abort(403)


class EducationView(MethodView):
    decorators = [login_required]
    page = f"dashboards/forms/education.html"

    def get(self):
        owner = current_user.profile
        form = EducationForm()
        educations = owner.education
        return render_template('dashboards/dashboard.html', page=self.page, form=form, educations=educations)

    def post(self):
        owner = current_user.profile
        form = EducationForm()

        if form.validate_on_submit():
            ed = Education(title=form.title.data, school=form.school.data, description=form.description.data,
                           duration=form.duration.data,
                           owner_id=owner.id)

            try:
                db.session.add(ed)
                db.session.commit()
                flash("اطلاعات با موفقیت ثبت شد.", 'success')
                return redirect(url_for('dashboards.educations'))


            except:
                flash("مشکلی پیش آمده است", 'danger')

        return render_template('dashboards/dashboard.html', page=self.page, form=form)


@login_required
def delete_edu():
    education_id = request.form.get('id')
    edu = Education.query.get_or_404(education_id)
    if edu.owner_id == current_user.id:
        db.session.delete(edu)
        db.session.commit()
        return jsonify({'message': 'Education deleted successfully'})
    abort(403)


class SkillView(MethodView):
    decorators = [login_required]
    page = f"dashboards/forms/skills.html"

    def get(self):
        owner = current_user.profile
        form = SkillForm()
        skills = owner.skill
        return render_template('dashboards/dashboard.html', page=self.page, form=form, skills=skills)

    def post(self):
        owner = current_user.profile
        form = SkillForm()

        if form.validate_on_submit():
            skill = Skill(name=form.name.data, percent=form.percent.data, owner_id=owner.id)

            try:
                db.session.add(skill)
                db.session.commit()
                flash("اطلاعات با موفقیت ثبت شد.", 'success')
                return redirect(url_for('dashboards.skills'))


            except:
                flash("مشکلی پیش آمده است", 'danger')

        return render_template('dashboards/dashboard.html', page=self.page, form=form)


@login_required
def delete_skill():
    skill_id = request.form.get('id')
    skill = Skill.query.get_or_404(skill_id)
    if skill.owner_id == current_user.id:
        db.session.delete(skill)
        db.session.commit()
        return jsonify({'message': 'Skill deleted successfully'})
    abort(403)


class PortfolioView(MethodView):
    decorators = [login_required]
    page = f"dashboards/forms/portfolio.html"

    def get(self):
        owner = current_user.profile
        form = PortfolioForm()
        portfolios = owner.portfolio
        return render_template('dashboards/dashboard.html', page=self.page, form=form, portfolios=portfolios)

    def post(self):
        owner = current_user.profile
        form = PortfolioForm()

        if form.validate_on_submit():
            portfolio = Portfolio(name=form.name.data, link=form.link.data, owner_id=owner.id)
            image = form.image.data
            if image:
                filename = secure_filename(image.filename)
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], 'portfolios', filename))
                portfolio.image = filename

            try:
                db.session.add(portfolio)
                db.session.commit()
                flash("اطلاعات با موفقیت ثبت شد.", 'success')
                return redirect(url_for('dashboards.portfolios'))


            except:
                flash("مشکلی پیش آمده است", 'danger')

        return render_template('dashboards/dashboard.html', page=self.page, form=form)


@login_required
def delete_portfolio():
    portfolio_id = request.form.get('id')
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    if portfolio.owner_id == current_user.id:
        db.session.delete(portfolio)
        db.session.commit()
        return jsonify({'message': 'Portfolio deleted successfully'})
    abort(403)


class ResumeView(MethodView):
    decorators = [login_required]
    page = f"dashboards/forms/build.html"

    def get(self):
        owner = current_user.profile
        visibility = owner.resume.is_visible
        public_pdf_download = owner.resume.public_pdf_download
        form = ResumeVisibilityForm()
        form.is_visible.data = visibility
        form.public_pdf_download.data = public_pdf_download
        return render_template('dashboards/dashboard.html', page=self.page, form=form)

    def post(self):
        owner = current_user.profile
        if len(owner.username) < 3:
            abort(403)
        form = ResumeVisibilityForm()
        if form.validate_on_submit():
            visibility = form.is_visible.data
            public_pdf_download = form.public_pdf_download.data
            owner.resume.is_visible = visibility
            owner.resume.public_pdf_download = public_pdf_download

            try:
                db.session.commit()
                flash("اطلاعات با موفقیت ثبت شد.", 'success')

                return redirect(url_for('dashboards.resume'))
            except:
                flash("مشکلی پیش آمده است", 'danger')

        return render_template('dashboards/dashboard.html', page=self.page, form=form)


blueprint.add_url_rule('/', view_func=ProfileUpdate.as_view('profile_update'), methods=["GET", "POST"])
blueprint.add_url_rule('/social', view_func=SocialUpdate.as_view('social_update'), methods=["GET", "POST"])
blueprint.add_url_rule('/experiences', view_func=WorkDataView.as_view('experiences'), methods=["GET", "POST"])
blueprint.add_url_rule('/educations', view_func=EducationView.as_view('educations'), methods=["GET", "POST"])
blueprint.add_url_rule('/skills', view_func=SkillView.as_view('skills'), methods=["GET", "POST"])
blueprint.add_url_rule('/portfolios', view_func=PortfolioView.as_view('portfolios'), methods=["GET", "POST"])
blueprint.add_url_rule('/resume', view_func=ResumeView.as_view('resume'), methods=["GET", "POST"])

blueprint.add_url_rule('/educations/delete', view_func=delete_edu, methods=["POST"])
blueprint.add_url_rule('/experiences/delete', view_func=delete_exp, methods=["POST"])
blueprint.add_url_rule('/skills/delete', view_func=delete_skill, methods=["POST"])
blueprint.add_url_rule('/portfolios/delete', view_func=delete_portfolio, methods=["POST"])
