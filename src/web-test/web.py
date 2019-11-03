import sys
import os
path = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))
sys.path.insert(0, '/home/hongyu/test/flask/src')
from flask import Flask, url_for, request, _request_ctx_stack
from blueprints.dev import bp
import flask 
print(flask.__file__)

app = Flask(__name__, subdomain_matching=True)

app.config['SERVER_NAME']="example.com:5000"

app.register_blueprint(bp)


def stream(environ, start_response):
    def s():
        for i in range(10):
            yield str(i).encode()
        start_response(200, None)
    return s()

#@app.after_request
def getresponse_data(response):
    data = response.get_data()
    print('response data:', data)
    response.set_data(''.join([i for i in reversed(data.decode())]).encode())
    headers = request.get_wsgi_headers()
    print(headers)
    return response

@app.route('/', endpoint='index')
def index():
    print(request.environ)
    print(_request_ctx_stack.top)
    print(app.url_map)
    return url_for('index', _external=True)
    # return app                                                                    # 这里可以返回一个可调用对象，但
    # return stream
    # 配置好 app.config['SERVER_NAME']="example.com:5000" 后输出 http://example.com:5000/ （测试的话需要修改host）

@app.route('/', subdomain='test', endpoint='test.index')
def test():
    print(request.url)
    print(app.url_map)
    print([i for i in app.url_map.iter_rules('index')])
    return url_for('test.index', _external=True)    # http://test.example.com:5000/


if __name__ == "__main__":
    app.run(debug=True)
