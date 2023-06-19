from flask import Blueprint, render_template, flash, redirect, url_for
from flask.views import MethodView
from flask_login import login_required, current_user

from .forms import ProfileForm
from app.extensions import db
from datetime import datetime

from .models import Profile

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

            try:
                db.session.commit()
                flash('پروفایل با موفقیت تفییر یافت.', 'success')
                return redirect(url_for('dashboards.profile_update'))
            except:
                flash('خطایی در هنگام انجام عملیات رخ داده است. لطفا مجددا امتحان کنید.', category='danger')

        return render_template('dashboards/dashboard.html', page=self.page, form=form)


blueprint.add_url_rule('/', view_func=ProfileUpdate.as_view('profile_update'), methods=["GET", "POST"])
