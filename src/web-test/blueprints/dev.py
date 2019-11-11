from flask import Blueprint, url_for, request

bp = Blueprint('dev-test', __name__, subdomain='dev')

@bp.route('/')
def index():
    print(request.environ)
    print(request.url)
    print(request.blueprint)
    print(request.form.getlist)
    return 'admin page, {}'.format(url_for('dev-test.index', _external=True))# url_for('.index') ‘.’ 会首先在当前 蓝图寻找


@bp.route('/abc/<string:id>')
def abc(id):
    print(request.environ)
    print(request.url)
    print(id)
    return 'admin page, {}'.format(url_for('dev-test.index', _external=True))# url_for('.index') ‘.’ 会首先在当前 蓝图寻找