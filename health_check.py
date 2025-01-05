from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import time
import json

# Store the start time when the module is loaded
start_time = time.time()

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')  # Allow CORS requests
            self.end_headers()
            current_time = time.time()
            up_time_seconds = current_time - start_time
            up_time_days = up_time_seconds // (24 * 3600)
            up_time = time.strftime(f'{int(up_time_days)} days %H hours %M minutes', time.gmtime(up_time_seconds))
            response = {
                'up_time': up_time
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.send_header('Access-Control-Allow-Origin', '*')  # Allow CORS requests for 404 responses
            self.end_headers()

def start_health_check_server():
    server_address = ('', 8000)  # Listen on all interfaces, port 8000
    httpd = HTTPServer(server_address, HealthCheckHandler)
    httpd.serve_forever()

def run_health_check_server():
    health_check_thread = threading.Thread(target=start_health_check_server)
    health_check_thread.daemon = True
    health_check_thread.start()