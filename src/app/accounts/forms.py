from wtforms import BooleanField
from flask_wtf import FlaskForm
from .models import User
from wtforms.validators import Length, DataRequired, EqualTo, ValidationError
from wtforms import PasswordField, SubmitField, EmailField


class SignupForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=8,
                                                                            message='رمز عبور باید بیشتر از 8 کارکتر باشد.')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password',
                                                                                             message="تکرار باید برابر با رمز عبور باشد.")])
    submit = SubmitField('ثبت نام')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError("این ایمیل از قبل وجود دارد.")


class SigninForm(FlaskForm):
    email = EmailField(validators=[DataRequired()])

    password = PasswordField(validators=[DataRequired()])
    remember_me = BooleanField()
    submit = SubmitField("ورود")


class PasswordResetForm(FlaskForm):
    email = EmailField(validators=[DataRequired()])
    submit = SubmitField("ارسال")


class SetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8,
                                                                            message='رمز عبور باید بیشتر از 8 کارکتر باشد.')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password',
                                                                                             message="تکرار باید برابر با رمز عبور باشد.")])
    submit = SubmitField('بازیابی رمز عبور')
