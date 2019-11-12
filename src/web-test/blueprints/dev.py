import mimetypes
from flask import Blueprint, url_for, request
from flask.helpers import send_file

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

@bp.route('/download')
def download():
    file_path = '/home/hongyu/500G-disk/备份/anaconda3.tar.gz'
    return send_file(filename_or_fp=file_path, mimetype=mimetypes.guess_type(file_path)[0], conditional=True, as_attachment=True)