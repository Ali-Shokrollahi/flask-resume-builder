from flask import Flask
from app.extensions import db, migrate

app = Flask(__name__)
app.config.from_object('config.DevConfig')

db.init_app(app)
migrate.init_app(app, db)
