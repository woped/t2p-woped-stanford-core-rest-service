import os
import socket
import re
import logging
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from pythonjsonlogger import jsonlogger
import sys

from nltk.parse.corenlp import CoreNLPParser
from nltk.parse.corenlp import CoreNLPServer

# Prometheus Metriken
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency', ['method', 'endpoint'])
PARSE_DURATION = Histogram('parse_duration_seconds', 'Time taken to parse text')

# Logging Setup
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Stdout handler with JSON formatter
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_formatter = jsonlogger.JsonFormatter(
    '%(asctime)s %(levelname)s %(name)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
stdout_handler.setFormatter(stdout_formatter)
logger.addHandler(stdout_handler)

logger.info("Logging setup completed successfully")

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress logging for /metrics endpoint
        if self.path == '/metrics':
            return
        super().log_message(format, *args)

    def do_GET(self):
        start_time = time.time()
        try:
            if self.path == '/metrics':
                self.send_response(200)
                self.send_header('Content-Type', CONTENT_TYPE_LATEST)
                self.end_headers()
                self.wfile.write(generate_latest())
                REQUEST_COUNT.labels(method='GET', endpoint='/metrics', status='200').inc()
            elif self.path == '/test-success':
                logger.info("Test success endpoint called")
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {"status": "success", "message": "Test successful"}
                self.wfile.write(str.encode(str(response)))
                REQUEST_COUNT.labels(method='GET', endpoint='/test-success', status='200').inc()
            elif self.path == '/test-error':
                logger.error("Test error endpoint called - generating 500 error")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {"status": "error", "message": "Test error response"}
                self.wfile.write(str.encode(str(response)))
                REQUEST_COUNT.labels(method='GET', endpoint='/test-error', status='500').inc()
            else:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'Service to create a tree from a single sentence')
                REQUEST_COUNT.labels(method='GET', endpoint='/', status='200').inc()
        except Exception as e:
            logger.error("Error in GET request: %s", str(e))
            REQUEST_COUNT.labels(method='GET', endpoint=self.path, status='500').inc()
            self.send_error(500, str(e))
        finally:
            REQUEST_LATENCY.labels(method='GET', endpoint=self.path).observe(time.time() - start_time)

    def do_POST(self):
        start_time = time.time()
        try:
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            body = body.decode("utf-8")
            
            logger.info("Received POST request with text", extra={"text": body})
            
            parse_start_time = time.time()
            parsed_body = nlpParser.parse(body.split())
            PARSE_DURATION.observe(time.time() - parse_start_time)
            
            ret = ""
            for elem in parsed_body:
                ret = ret + str(elem)
            
            logger.info("Parsing result", extra={"result": ret})
            
            self.send_response(200)
            self.end_headers()
            response = BytesIO()
            response.write(str.encode(ret))
            self.wfile.write(response.getvalue())
            REQUEST_COUNT.labels(method='POST', endpoint='/', status='200').inc()
        except Exception as e:
            logger.error("Error in POST request", extra={"error": str(e)})
            REQUEST_COUNT.labels(method='POST', endpoint='/', status='500').inc()
            self.send_error(500, str(e))
        finally:
            REQUEST_LATENCY.labels(method='POST', endpoint='/').observe(time.time() - start_time)

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def run(server_class=HTTPServer, handler_class=Handler):
    server_address = ('', 8083)
    httpd = server_class(server_address, handler_class)
    logger.info("Starting server on port 8083")
    httpd.serve_forever()

jar_path = "/jars"
stanford_jar_pattern = r'^stanford\-corenlp\-\d+\.\d+\.\d+\.jar$'
stanford_models_pattern = r'^stanford\-corenlp\-\d+\.\d+\.\d+\-models\.jar$'

pathname1 = ""
pathname2 = ""

logger.info("Starting JAR search in directory: %s", jar_path)

if not os.path.exists(jar_path):
    logger.error("JAR directory does not exist: %s", jar_path)
    raise FileNotFoundError(f"JAR directory not found: {jar_path}")

try:
    # First, list all directories
    jar_dirs = [d for d in os.listdir(jar_path) if os.path.isdir(os.path.join(jar_path, d))]
    logger.info("Found directories in JAR directory: %s", jar_dirs)
    
    # Search in each directory
    for dir_name in jar_dirs:
        dir_path = os.path.join(jar_path, dir_name)
        logger.info("Searching in directory: %s", dir_path)
        
        try:
            files = os.listdir(dir_path)
            logger.info("Files in directory %s: %s", dir_path, files)
            
            for file_name in files:
                file_path = os.path.join(dir_path, file_name)
                if os.path.isfile(file_path):
                    logger.debug("Checking file: %s", file_path)
                    if re.match(stanford_jar_pattern, file_name):
                        logger.info("Found CoreNLP JAR: %s", file_path)
                        pathname1 = file_path
                    elif re.match(stanford_models_pattern, file_name):
                        logger.info("Found CoreNLP Models JAR: %s", file_path)
                        pathname2 = file_path
        except Exception as e:
            logger.error("Error reading directory %s", dir_path, extra={"error": str(e)})
            continue
except Exception as e:
    logger.error("Error searching for JAR files", extra={"error": str(e)})
    raise

if not pathname1:
    logger.error("Could not find CoreNLP JAR file")
    raise FileNotFoundError("CoreNLP JAR file not found")
if not pathname2:
    logger.error("Could not find CoreNLP Models JAR file")
    raise FileNotFoundError("CoreNLP Models JAR file not found")

logger.info("CoreNLP JAR path: %s", pathname1)
logger.info("CoreNLP Models JAR path: %s", pathname2)

if is_port_in_use(9000):
    logger.warning("Port 9000 is already in use")
else:
    logger.info("Port 9000 is available")

nlpServer = CoreNLPServer(path_to_jar=pathname1,
                         path_to_models_jar=pathname2,
                         port=9000)

nlpParser = CoreNLPParser(url="http://localhost:9000")

if not is_port_in_use(9000):
    logger.info("Starting CoreNLP server on port 9000")
    nlpServer.start()
else:
    logger.warning("Port 9000 is already in use")

run()

