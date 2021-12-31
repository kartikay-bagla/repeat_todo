from flask import Blueprint
from flask_login import current_user, login_required

main_route = Blueprint('main', __name__)


@main_route.route('/')
def index():
    return "Hello World!"


@main_route.route('/user')
@login_required
def user():
    return "Hello, %s" % current_user.username
