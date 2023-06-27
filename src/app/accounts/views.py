from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask.views import MethodView
from flask_login import login_user, logout_user

from .forms import SignupForm, SigninForm
from .models import User
from .token import generate_token, confirm_token
from app.extensions import db
from app.utils.email import send_email
from app.utils.decorators import redirect_authenticated_user
from ..dashboards.models import Profile
from ..resumes.models import Resume

blueprint = Blueprint('accounts', __name__, url_prefix='/account', template_folder='templates/accounts')


class SignupUser(MethodView):
    decorators = [redirect_authenticated_user]

    def get(self):
        form = SignupForm()

        return render_template('accounts/signup.html', form=form)

    def post(self):
        form = SignupForm()
        if form.validate_on_submit():
            user = User(email=form.email.data)
            user.set_user_password(form.password.data)

            db.session.add(user)

            token = generate_token(user.email)
            confirm_url = url_for("accounts.confirm_email", token=token, _external=True)
            html = render_template("accounts/confirm_email.html", confirm_url=confirm_url)
            subject = "لطفا ایمیل خود را تایید کنید."
            send_email(user.email, subject, html)
            db.session.flush()
            profile = Profile(user_id=user.id)
            resume = Resume(owner_id=user.id)
            db.session.add(profile)
            db.session.add(resume)
            db.session.commit()
            return redirect(url_for("accounts.signup_success"))

            flash('خطایی در هنگام انجام عملیات رخ داده است. لطفا مجددا امتحان کنید.', category='danger')

        return render_template('accounts/signup.html', form=form)


def confirm_email(token: str):
    email = confirm_token(token)
    user = User.query.filter_by(email=email).first_or_404()
    if user.email == email:
        user.email_verified = True
        user.is_active = True
        db.session.commit()
        flash("ایمیل شما با موفقیت تایید شد! لطفا به حساب خود وارد شوید.", "success")
        return redirect(url_for("accounts.signin"))


    else:
        flash("این لینک غیرمعتبر با منقضی شده است.", "danger")

    return redirect(url_for("accounts.signup"))


@redirect_authenticated_user
def signup_success():
    return render_template('accounts/signup_success.html')


class SigninUser(MethodView):
    decorators = [redirect_authenticated_user]

    def get(self):
        form = SigninForm()
        return render_template('accounts/signin.html', form=form)

    def post(self):
        form = SigninForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_user_password(form.password.data):
                if not user.email_verified:
                    flash("لطفا ابتدا ایمیل خود را تایید نمایید.", "warning")

                elif not user.is_active:
                    flash("این کاربر مجور ورود ندارد.", "warning")


                else:
                    remember_me = form.remember_me.data
                    login_user(user, remember=remember_me)

                    flash("ورود با موفقیت انجام شد.", "success")
                    return redirect(url_for("dashboards.profile_update"))

            else:
                flash("ایمیل یا رمز عبور نامعتبر است. لطفاً مجدداً تلاش کنید.", "danger")

        return render_template('accounts/signin.html', form=form)


def logout():
    logout_user()
    flash('شما از حساب خود خارج شدید!.', 'warning')
    return redirect(url_for('accounts.signin'))


blueprint.add_url_rule('/signup', view_func=SignupUser.as_view('signup'), methods=["GET", "POST"])
blueprint.add_url_rule('/confirm/<string:token>', view_func=confirm_email, methods=["GET"])
blueprint.add_url_rule('/signup/success', view_func=signup_success, methods=["GET"])
blueprint.add_url_rule('/signin', view_func=SigninUser.as_view('signin'), methods=["GET", "POST"])
blueprint.add_url_rule('/logout/', view_func=logout, methods=["POST"])
