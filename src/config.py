import os

from decouple import config


class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = config('SECRET_KEY', default='test_project')


class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ...


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(Config.BASE_DIR, 'app.db')
