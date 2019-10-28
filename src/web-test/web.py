from flask import Flask, url_for, request
from blueprints.dev import bp

app = Flask(__name__, subdomain_matching=True)

app.config['SERVER_NAME']="example.com:5000"

app.register_blueprint(bp)

@app.route('/')
def index():
    print(request.url)
    print(app.url_map)
    return url_for('index', _external=True)   

@app.route('/', subdomain='test')
def test():
    print(request.url)
    print(app.url_map)
    return url_for('test', _external=True)   
    # 输出 http://127.0.0.1:5000/；
    # 配置好 app.config['SERVER_NAME']="example.com:5000" 后输出 http://example.com:5000/ （测试的话需要修改host）



if __name__ == "__main__":
    app.run(debug=True)
