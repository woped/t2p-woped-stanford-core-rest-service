import os
import socket
import re
import logging

from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO

from nltk.parse.corenlp import CoreNLPParser
from nltk.parse.corenlp import CoreNLPServer

logging.basicConfig(level=logging.INFO)

class Handler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        if self.path == '/metrics':
            return
        super().log_message(format, *args)

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
        logging.info(ret)
        response.write(str.encode(ret))
        self.wfile.write(response.getvalue())

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def run(server_class=HTTPServer, handler_class=Handler):
    server_address = ('', 8083)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

jar_path = "/jars"
stanford_jar_pattern = r'^stanford\-corenlp\-\d+\.\d+\.\d+\.jar$'
stanford_models_pattern = r'^stanford\-corenlp\-\d+\.\d+\.\d+\-models\.jar$'

pathname1 = ""
pathname2 = ""

logging.debug(os.listdir(jar_path))

for path in os.scandir(jar_path):
    logging.debug("jars-dir content: " + path.path)
    if path.is_dir and not re.match("^.*\.zip$", path.name):
        logging.debug ("The path.name is " + path.name)
        for file in os.scandir(path.path):
            if file.is_file:
                logging.debug ("The file.name is " + file.name)
                if re.match(stanford_jar_pattern, file.name):
                    logging.debug ("Setting pathname1")
                    pathname1 = file.path
                if re.match(stanford_models_pattern, file.name):
                    logging.debug ("Setting pathname2")
                    pathname2 = file.path

logging.info ("pathname1: <" + pathname1 + ">")
logging.info ("pathname2: <" + pathname2 + ">")

nlpServer = CoreNLPServer(path_to_jar=pathname1,
                          path_to_models_jar=pathname2,
                          port=9000)

nlpParser = CoreNLPParser(url="http://localhost:9000")

if is_port_in_use(9000) is False:
    nlpServer.start()
run()

