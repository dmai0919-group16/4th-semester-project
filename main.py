from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

server_host = 'localhost'
server_port = 8081 

response_path = None

class StoppableHttpServer (HTTPServer):
    def serve_forever (self):
        self.stop = False
        while not self.stop:
            self.handle_request()

class DummyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global response_path
        path = self.path

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(bytes("%s" % path, "utf-8"))

        if('?code=' in path):
            response_path = path
            self.server.stop = True


if __name__ == '__main__':
    print('[*] Starting web server (on %s:%i) to catch login redirect' % (server_host, server_port))
    httpd = StoppableHttpServer((server_host, server_port), DummyRequestHandler)
    httpd.serve_forever()
    httpd.server_close()

    print('[*] Caught URL with auth token %s', response_path)
    
