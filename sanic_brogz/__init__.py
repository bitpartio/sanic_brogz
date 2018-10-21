import gzip
from pprint import pprint
import brotli

DEFAULT_MIME_TYPES = frozenset([
    'text/html', 'text/css', 'text/xml',
    'application/json',
    'application/javascript'])


class Compress(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        defaults = [
            ('COMPRESS_MIMETYPES', DEFAULT_MIME_TYPES),
            ('COMPRESS_LEVEL', 6),
            ('COMPRESS_MIN_SIZE', 500),
        ]

        for k, v in defaults:
            app.config.setdefault(k, v)

        @app.middleware('response')
        async def compress_response(request, response):
            return (await self._compress_response(request, response))

    async def _compress_response(self, request, response):
        accept_encoding = request.headers.get('Accept-Encoding', '')

        accepted = [w.strip() for w in accept_encoding.split(',')]

        content_length = len(response.body)
        content_type = response.content_type

        if ';' in response.content_type:
            content_type = content_type.split(';')[0]

        if (content_type not in self.app.config['COMPRESS_MIMETYPES'] or
            ('br' not in accepted and
             'gzip' not in accepted) or
            not 200 <= response.status < 300 or
            (content_length is not None and
             content_length < self.app.config['COMPRESS_MIN_SIZE']) or
                'Content-Encoding' in response.headers):
            return response

        if 'br' in accepted:
            compressed_content = self.br(response)
            response.headers['Content-Encoding'] = 'br'

        elif 'gzip' in accepted:
            compressed_content = self.gz(response)
            response.headers['Content-Encoding'] = 'gzip'

        response.body = compressed_content

        response.headers['Content-Length'] = len(response.body)

        vary = response.headers.get('Vary')
        if vary:
            if 'accept-encoding' not in vary.lower():
                response.headers['Vary'] = '{}, Accept-Encoding'.format(vary)
        else:
            response.headers['Vary'] = 'Accept-Encoding'

        return response

    def gz(self, response):
        out = gzip.compress(
            response.body,
            compresslevel=self.app.config['COMPRESS_LEVEL'])

        return out

    def br(self, response):
        out = brotli.compress(response.body, quality=self.app.config['COMPRESS_LEVEL'])

        return out
