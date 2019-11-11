import sys
import os
path = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))
sys.path.insert(0, '/home/hongyu/test/flask/src')
from flask import Flask, url_for, request, _request_ctx_stack, g, _app_ctx_stack, current_app
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
    print('- - '*10)
    print(request.environ)
    print(_request_ctx_stack.top)
    print(app.url_map)

    adapter = app.create_url_adapter(request)
    print(adapter.test('/', method='POST'))                                         # False
    print(adapter.match(return_rule=True))
    print(_app_ctx_stack.top.g == g)                                                # True , but not is
    print('g:::::',_app_ctx_stack.top.g.__dict__, g.__dict__)
    print(request == _request_ctx_stack.top.request)                                # True
    print('- - '*10)
    response = app.make_response(url_for('index', _external=True))
    l = lambda: sum([len(_) for _ in response.response])
    response.make_conditional(request, accept_ranges=True, complete_length=l())  
    print(response.content_range)                                                   # bytes 0-20/24
    print('cache_control:{}'.format(response.cache_control))
    print('accept_ranges:',response.accept_ranges)                                  # bytes
    #response.freeze()
    #print(response.response)                                                       # 响应内容
    print(response.get_wsgi_headers(request))
    @response.call_on_close
    def func():
        print('response 关闭了!')

    return response
    # return app                                                                    # 这里可以返回一个可调用对象，但
    # return stream
    # 配置好 app.config['SERVER_NAME']="example.com:5000" 后输出 http://example.com:5000/ （测试的话需要修改host）

@app.url_value_preprocessor
def url_value_handle(endpoint, value):
    if value.get('lange_code', None):
        g.setdefault('lange_code', value.pop('lange_code'))


@app.url_defaults
def add_language_code(endpoint, value):
    if 'lange_code' in value or not g.get('lange_code', None):
        return
    
    if app.url_map.is_endpoint_expecting(endpoint, 'lange_code'):
        value['lange_code'] = g.get('lange_code')

@app.route('/lang/<string:lange_code>')
def lang():
    print(g.get('lange_code'))
    return url_for('lang', lange_code=g.get('lange_code'))

@app.route('/lang/<string:lange_code>/about')
def about():
    print('about {}'.format(g.get('lange_code')))
    return url_for('about')

@app.route('/', subdomain='test', endpoint='test.index')
def test():
    print(request.url)
    print(app.url_map)
    print([i for i in app.url_map.iter_rules('index')])
    print('===='*20)
    print(current_app.__dict__)
    return url_for('test.index', _external=True)    # http://test.example.com:5000/




if __name__ == "__main__":
    app.run(debug=True)
