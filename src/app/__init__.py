from flask import Flask

from app.accounts.models import User
from app.commands import admin_cli
from app.extensions import db, migrate, bcrypt, login_manager
from app.accounts.views import blueprint as account_blueprint


def register_blueprints(app):
    app.register_blueprint(account_blueprint)


def register_shell_context(app):
    def shell_context():
        return {
            'db': db,
            'User': User,

        }

    app.shell_context_processor(shell_context)


app = Flask(__name__)
app.config.from_object('config.DevConfig')

register_blueprints(app)
register_shell_context(app)
app.cli.add_command(admin_cli)

db.init_app(app)
bcrypt.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)

from app.accounts.models import User

login_manager.login_view = "accounts.login"
login_manager.login_message_category = "danger"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()
