from wtforms import BooleanField
from wtforms_alchemy import ModelForm
from flask_wtf import FlaskForm
from .models import User
from wtforms.validators import Length, DataRequired, EqualTo
from wtforms.fields import PasswordField, SubmitField, EmailField


class SignupForm(ModelForm, FlaskForm):
    class Meta:
        model = User
        only = ['email', 'password']

    password = PasswordField('Password', validators=[DataRequired(), Length(min=8,
                                                                            message='رمز عبور باید بیشتر از 8 کارکتر باشد.')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password',
                                                                                             message="تکرار باید برابر با رمز عبور باشد.")])
    submit = SubmitField('ثبت نام')


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
