import os

from decouple import config


class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = config('SECRET_KEY', default='test_project')
    SECURITY_PASSWORD_SALT = config('SECURITY_PASSWORD_SALT', default='very-important')

    # Mail sending
    MAIL_DEFAULT_SENDER = 'ali@mailtrap.io'
    MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = config("EMAIL_USER")
    MAIL_PASSWORD = config("EMAIL_PASSWORD")

    # uploads
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app/static/uploads')


class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ...


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(Config.BASE_DIR, 'app.db')
