from flask import Blueprint

blueprint = Blueprint('users', __name__, url_prefix='/account', template_folder='templates/accounts')
