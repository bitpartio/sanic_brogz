# sanic_brogz

sanic_brogz is an extension which allows you to easily brotli compress or gzip your Sanic responses. It is a fork of the [sanic_compress](https://github.com/subyraman/sanic_compress) package which is a port of the [Flask-Compress](https://github.com/libwilliam/flask-compress) extension.


## Installation

Install with `pip`:

`pip install sanic_brogz`

## Usage

Usage is simple. Simply pass in the Sanic app object to the `Compress` class, and responses will be brotli compressed or gzipped.

```python
from sanic import Sanic
from sanic_brogz import Compress

app = Sanic(__name__)
Compress(app)
```

## Options

Within the Sanic application config you can provide the following settings to control the behavior of sanic_brogz. None of the settings are required.


`COMPRESS_MIMETYPES`: Set the list of mimetypes to compress here.
- Default: `{'text/html','text/css','text/xml','application/json','application/javascript'}`

`COMPRESS_LEVEL`: Specifies the gzip compression level (1-9) or brotli compression level (1-11).
- Default: `6`

`COMPRESS_MIN_SIZE`: Specifies the minimum size (in bytes) threshold for compressing responses.
- Default: `500`

A higher `COMPRESS_LEVEL` will result in a gzipped response that is smaller, but the compression will take longer.

Example of using custom configuration:

```python
from sanic import Sanic
from sanic_brogz import Compress

app = Sanic(__name__)
app.config['COMPRESS_MIMETYPES'] = {'text/html', 'application/json'}
app.config['COMPRESS_LEVEL'] = 4
app.config['COMPRESS_MIN_SIZE'] = 300
Compress(app)
```

### Note about compressing static files:

Sanic is not at heart a file server. You should consider serving static files with nginx or on a separate file server.
