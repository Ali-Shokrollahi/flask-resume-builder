from flask import Blueprint, render_template
from flask.views import MethodView
from .forms import SignupForm
from .models import User
from app.extensions import db

blueprint = Blueprint('users', __name__, url_prefix='/account', template_folder='templates/accounts')


# def register():
#     form = SignupForm
#     if request.method == "POST":
#         if form.validate_on_submit():
#             user = model.User(name=form.name.data, lastname=form.lastname.data, email=form.email.data,
#                               password=form.password.data)
#
#             db.session.add(user)
#             db.session.commit()
#             sleep(1)
#
#             flash("شما با موفقیت ثبت نام شدید! جهت استفاده از خدمات به سایت وارد شوید.", "تمام")
#             return redirect(url_for('login'))
#         else:
#             flash("مشکلی پیش آمده، لطفا مجددا تلاش نمیایید.", "خطا")
#
#     return render_template('register.html', form=form)

class SigninUser(MethodView):
    def get(self):
        form = SignupForm()
        return render_template('accounts/signup.html', form=form)

    def post(self):
        form = SignupForm()
        if form.validate_on_submit():
            user = User(email=form.email.data)
            user.set_user_password(form.password.data)
            db.session.add(user)
            db.session.commit()

        return render_template('accounts/signup.html', form=form)


blueprint.add_url_rule('/signup', view_func=SigninUser.as_view('signin'), methods=["GET", "POST"])
