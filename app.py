from sanic import Sanic
import string
import random
from sanic.response import json, html, HTTPResponse
from sanic_brogz import Compress

app = Sanic('compressed')
Compress(app)


@app.route('/json/<length>')
def j(request, length):
    data = {'a': "".join(['b'] * (int(length) - 8))}
    return json(data)


@app.route('/')
def h(request):
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15000))
    return html(res)


@app.route('/html/status/<status>')
def h_with_status(request, status):
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15000))
    return html(res, status=int(status))


@app.route('/html/vary/<vary>')
def h_with_vary(request, vary):
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15000))
    return html(res, headers={'Vary': vary})


@app.route('/other/<length>')
def other(request, length):
    content_type = request.args.get('content_type')
    body = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return HTTPResponse(
        body, content_type=content_type)

app.run()
