from flask import Blueprint, render_template

blueprint = Blueprint('home', __name__)


def index():
    return render_template('home/index.html')


blueprint.add_url_rule('/', view_func=index, methods=["GET"])
