from flask import Blueprint, url_for, request

bp = Blueprint('dev-test', __name__, subdomain='dev')

@bp.route('/')
def index():
    print(request.url)
    return 'admin page, {}'.format(url_for('dev-test.index', _external=True))