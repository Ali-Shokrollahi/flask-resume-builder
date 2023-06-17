from flask import Flask
from app.extensions import db, migrate
from app.accounts.views import blueprint as account_blueprint


def register_blueprints(app: Flask):
    app.register_blueprint(account_blueprint)


app = Flask(__name__)
app.config.from_object('config.DevConfig')

db.init_app(app)
migrate.init_app(app, db)
