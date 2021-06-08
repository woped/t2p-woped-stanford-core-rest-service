import os
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO

from nltk.parse.corenlp import CoreNLPParser
from nltk.parse.corenlp import CoreNLPServer


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Service to create a tree from a single sentence')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        body = body.decode("utf-8")
        body = nlpParser.parse(body.split())
        ret = ""
        for elem in body:
            ret = ret + str(elem)
        print(ret)
        response.write(str.encode(ret))
        self.wfile.write(response.getvalue())


pathname1 = os.path.join("jars", "stanford-corenlp-4.2.1.jar")
pathname2 = os.path.join("jars", "stanford-corenlp-4.2.1-models.jar")
nlpServer = CoreNLPServer(path_to_jar=pathname1,
                          path_to_models_jar=pathname2,
                          port=9000)


def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


nlpParser = CoreNLPParser(url="http://localhost:9000")

if is_port_in_use(9000) is False:
    nlpServer.start()


def run(server_class=HTTPServer, handler_class=Handler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


run()
