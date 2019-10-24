from flask import Blueprint, url_for

bp = Blueprint('dev-test', __name__, subdomain='dev')

@bp.route('/')
def index():
    return 'admin page, {}'.format(url_for('dev-test.index', _external=True))