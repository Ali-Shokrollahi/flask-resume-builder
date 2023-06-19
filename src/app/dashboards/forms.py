from flask_wtf import FlaskForm
from wtforms.fields import EmailField
from wtforms import PasswordField, SubmitField, SelectField, StringField
from wtforms.validators import DataRequired, Length, EqualTo, Optional
from wtforms_alchemy import ModelForm

from app.dashboards.models import Profile


class ProfileForm(ModelForm, FlaskForm):
    class Meta:
        model = Profile
        only = ['first_name', 'last_name', 'username', 'job', 'bio', 'photo']

    gender = SelectField(choices=["مرد", "زن"], validators=[Optional()])
    birthday = StringField(validators=[Optional()])

    submit = SubmitField('ثبت نام')
