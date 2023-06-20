from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField
from wtforms.validators import DataRequired, Length, Optional, Regexp, ValidationError
from wtforms_alchemy import ModelForm

from app.dashboards.models import Profile, Social


class ProfileForm(ModelForm, FlaskForm):
    class Meta:
        model = Profile
        only = ['first_name', 'last_name', 'job', 'bio', 'photo']

    username = StringField('Username', validators=[DataRequired(), Length(min=3,
                                                                          message='نام کاربری باید بیشتر از 3 کارکتر باشد.'),
                                                   Regexp('^[A-Za-z0-9_]*$',
                                                          message='نام کاربری تنها می تواند شامل حروف و اعداد انگلیسی و خط تیره( _ ) باشد.')])

    gender = SelectField(choices=["مرد", "زن"], validators=[Optional()])
    birthday = StringField(validators=[Optional()])

    submit = SubmitField('تغییر اطلاعات')

    def validate_username(self, username):
        profile = Profile.query.filter_by(username=username.data).first()
        if profile:
            if current_user.profile != profile:
                raise ValidationError("این نام کاربری وجود دارد.")


class SocialForm(ModelForm, FlaskForm):
    class Meta:
        model = Social
        only = ['instagram', 'github', 'telegram', 'linkedin', 'pinterest', 'address']

    submit = SubmitField('تغییر اطلاعات')