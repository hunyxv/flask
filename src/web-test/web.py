from flask import Flask, url_for, request
from blueprints.dev import bp

app = Flask(__name__, subdomain_matching=True)

app.config['SERVER_NAME']="example.com:5000"

app.register_blueprint(bp)

@app.route('/', endpoint='index')
def index():
    print(request.url)
    print(app.url_map)
    return url_for('index', _external=True)
    # 配置好 app.config['SERVER_NAME']="example.com:5000" 后输出 http://example.com:5000/ （测试的话需要修改host）

@app.route('/', subdomain='test', endpoint='test.index')
def test():
    print(request.url)
    print(app.url_map)
    print([i for i in app.url_map.iter_rules('index')])
    return url_for('test.index', _external=True)    # http://test.example.com:5000/


if __name__ == "__main__":
    app.run(debug=True)
