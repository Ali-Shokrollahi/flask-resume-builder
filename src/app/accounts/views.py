from flask import Blueprint, render_template, flash, redirect, url_for
from flask.views import MethodView
from .forms import SignupForm
from .models import User
from .token import generate_token, confirm_token
from app.extensions import db
from app.utils.email import send_email

blueprint = Blueprint('accounts', __name__, url_prefix='/account', template_folder='templates/accounts')


class SignupUser(MethodView):
    def get(self):
        form = SignupForm()
        return render_template('accounts/signup.html', form=form)

    def post(self):
        form = SignupForm()
        if form.validate_on_submit():
            user = User(email=form.email.data)
            user.set_user_password(form.password.data)
            try:
                db.session.add(user)
                db.session.commit()
                token = generate_token(user.email)
                confirm_url = url_for("accounts.confirm_email", token=token, _external=True)
                html = render_template("accounts/confirm_email.html", confirm_url=confirm_url)
                subject = "لطفا ایمیل خود را تایید کنید."
                send_email(user.email, subject, html)
            except:
                flash('خطایی در هنگام انحام عملیات رخ داده است. لطفا مجددا امتحان کنید.')

            return redirect(url_for("accounts.signup"))

        return render_template('accounts/signup.html', form=form)


def confirm_email(token: str):
    # if current_user.is_confirmed:
    #     flash("Account already confirmed.", "success")
    #     return redirect(url_for("core.home"))
    email = confirm_token(token)
    user = User.query.filter_by(email=email).first_or_404()
    if user.email == email:
        user.email_verified = True
        user.is_active = True
        db.session.add(user)
        db.session.commit()
        flash("ایمیل شما با موفقیت تایید شد! لطفا به حساب خود وارد شوید.", "success")
    else:
        flash("این لینک غیرمعتبر با منقضی شده است.", "danger")
    return redirect(url_for("accounts.signup"))



blueprint.add_url_rule('/signup', view_func=SigninUser.as_view('signup'), methods=["GET", "POST"])
blueprint.add_url_rule('/confirm/<string:token>', view_func=confirm_email, methods=["GET"])
