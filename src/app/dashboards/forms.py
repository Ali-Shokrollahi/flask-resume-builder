from uuid import uuid4

from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import SubmitField, SelectField, StringField, IntegerField, HiddenField, FileField, BooleanField
from wtforms.validators import DataRequired, Length, Optional, Regexp, ValidationError, NumberRange
from wtforms_alchemy import ModelForm

from app.dashboards.models import Profile, Social, WorkData, Experience, Education, Skill, Portfolio


class ProfileForm(ModelForm, FlaskForm):
    class Meta:
        model = Profile
        only = ['first_name', 'last_name', 'job', 'bio', 'photo']

    username = StringField('Username', validators=[Optional(), Length(min=3,
                                                                      message='نام کاربری باید بیشتر از 3 کارکتر باشد.'),
                                                   Regexp('^[A-Za-z0-9_]*$',
                                                          message='نام کاربری تنها می تواند شامل حروف و اعداد انگلیسی و خط تیره( _ ) باشد.')])

    gender = SelectField(choices=["مرد", "زن"], validators=[Optional()])
    birthday = StringField(validators=[Optional()])
    photo = FileField(
        validators=[Optional(),
                    FileAllowed(['jpg', 'jpeg', 'png'], message="فایل مجاز نیست. فایل های مجاز (png, jpg, jpeg)")])

    submit = SubmitField('تغییر اطلاعات')

    def validate_username(self, username):
        profile = Profile.query.filter_by(username=username.data).first()
        if profile:
            if current_user.profile != profile:
                raise ValidationError("این نام کاربری وجود دارد.")

    def validate_photo(self, field):
        if field.data:
            filename = str(field.data.filename)
            ext = filename.split(".")[-1].lower()
            new_name = f"{str(uuid4())}.{ext}"
            field.data.filename = new_name


class SocialForm(ModelForm, FlaskForm):
    class Meta:
        model = Social
        only = ['instagram', 'github', 'telegram', 'linkedin', 'pinterest', 'address']

    submit = SubmitField('تغییر اطلاعات')


class WorkDataForm(FlaskForm):
    experience = IntegerField(validators=[DataRequired(), NumberRange(min=0, max=64)])
    number_of_projects = IntegerField(validators=[DataRequired(), NumberRange(min=0, max=64)])
    number_of_customer = IntegerField(validators=[DataRequired(), NumberRange(min=0, max=64)])
    submit = SubmitField('بروزرسانی')


class ExperienceForm(ModelForm, FlaskForm):
    class Meta:
        model = Experience
        only = ['title', 'company', 'description', 'duration']

    duration = IntegerField(validators=[DataRequired(), NumberRange(min=0, max=64)])

    submit = SubmitField('اضافه کردن')


class EducationForm(ModelForm, FlaskForm):
    class Meta:
        model = Education
        only = ['title', 'school', 'description', 'duration']

    duration = IntegerField(validators=[DataRequired(), NumberRange(min=0, max=64)])

    submit = SubmitField('اضافه کردن')


class SkillForm(ModelForm, FlaskForm):
    class Meta:
        model = Skill
        only = ['name', 'percent']

    submit = SubmitField('اضافه کردن')


class ResumeVisibilityForm(FlaskForm):
    is_visible = BooleanField('وضعیت نمایش')
    public_pdf_download = BooleanField('قابلیت دانلود همگانی رزومه')
    submit = SubmitField('ثبت')


class PortfolioForm(ModelForm, FlaskForm):
    class Meta:
        model = Portfolio
        only = ['name', 'link', 'image']

    image = FileField(
        validators=[Optional(),
                    FileAllowed(['jpg', 'jpeg', 'png'], message="فایل مجاز نیست. فایل های مجاز (png, jpg, jpeg)")])

    submit = SubmitField('اضافه کردن')

    def validate_image(self, field):
        if field.data:
            filename = str(field.data.filename)
            ext = filename.split(".")[-1].lower()
            new_name = f"{str(uuid4())}.{ext}"
            field.data.filename = new_name
