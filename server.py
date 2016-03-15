import os
from read_sensor import Control

try:
    from SimpleHTTPServer import SimpleHTTPRequestHandler as Handler
    from SocketServer import TCPServer as Server
except ImportError:
    from http.server import SimpleHTTPRequestHandler as Handler
    from http.server import HTTPServer as Server

class MyHandler(Handler):
    def do_HEAD(self):
        print("do_HEAD()");
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        """Respond to a GET request."""
        print("do_GET()");
        Handler.do_GET(self)

# Read port selected by the cloud for our application
PORT = int(os.getenv('PORT', 8000))

# Change current directory to avoid exposure of control files
os.chdir('static')

control = Control()
httpd = Server(("", PORT), MyHandler)
try:
    print("Start serving at port %i" % PORT)
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()

