from functools import wraps

from flask import redirect, url_for
from flask_login import current_user


def redirect_authenticated_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('dashboards.profile_update'))  # Replace 'dashboards' with your actual dashboards route
        return f(*args, **kwargs)

    return decorated_function
