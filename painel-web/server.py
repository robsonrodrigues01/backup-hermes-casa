#!/usr/bin/env python3
# Painel do escritório (estático) + proxy /dash/* -> localhost:8800 (prefixo /dash removido, como o Caddy faz).
# A chave k é injetada aqui no servidor: nunca aparece no HTML que vai pro navegador.
import http.server, urllib.request, urllib.error, os, re

ROOT = '/home/hermes/painel-web'
KEY = '6a50de16401166fc3c52052242b612c3'
UP = 'http://127.0.0.1:8800'
INJECT_FROM = b"new URLSearchParams(location.search).get('k')||''"
INJECT_TO = b"'" + KEY.encode() + b"'"

class H(http.server.BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def _static(self):
        path = self.path.split('?')[0]
        if path == '/':
            path = '/index.html'
        f = os.path.normpath(ROOT + path)
        if not f.startswith(ROOT) or not os.path.isfile(f):
            self.send_error(404, 'arquivo'); return
        data = open(f, 'rb').read()
        ct = 'text/html; charset=utf-8' if f.endswith('.html') else 'application/octet-stream'
        self.send_response(200)
        self.send_header('Content-Type', ct)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(data)

    def _proxy(self):
        rest = self.path[len('/dash'):] or '/'
        if '?' in rest:
            url = UP + rest
        else:
            url = UP + rest + '?k=' + KEY
        if not re.search(r'[?&]k=', url):
            url += '&k=' + KEY
        req = urllib.request.Request(url, method=self.command)
        ln = int(self.headers.get('Content-Length') or 0)
        if ln:
            req.data = self.rfile.read(ln)
        if self.headers.get('Content-Type'):
            req.add_header('Content-Type', self.headers['Content-Type'])
        try:
            r = urllib.request.urlopen(req, timeout=20)
            body, code, hdrs = r.read(), r.status, r.headers
        except urllib.error.HTTPError as e:
            body, code, hdrs = e.read(), e.code, e.headers
        except Exception as ex:
            self.send_error(502, str(ex)); return
        ct = hdrs.get('Content-Type', 'text/plain')
        if 'html' in ct and INJECT_FROM in body:
            body = body.replace(INJECT_FROM, INJECT_TO, 1)
        self.send_response(code)
        self.send_header('Content-Type', ct)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def _route(self):
        if self.path.split('?')[0].startswith('/dash'):
            self._proxy()
        else:
            self._static()

    def do_GET(self): self._route()
    def do_POST(self): self._route()
    def do_HEAD(self): self._route()
    def log_message(self, format, *args): pass

http.server.ThreadingHTTPServer(('0.0.0.0', 8643), H).serve_forever()
