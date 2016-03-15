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
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        """Respond to a GET request."""
        #Handler.do_GET(self)
        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        print("Sending some html data now ...")

        self.wfile.write(("<head>" +
                          "  <title>Python Starter Application</title>" +
                          "  <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">" +
                          "  <link rel=\"stylesheet\" href=\"stylesheets/style.css\"/>" +
                          "</head>").encode('utf-8'))
        self.wfile.write(("<body><table><tr>" + 
                          "<td style='width: 30%;'>" + 
                          "  <img class='newappIcon' src='images/newapp-icon.png'>" +
                          "</td>" +
                          "<td>").encode('utf-8'))

        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        for i in range(0, control.getMaxMessage()):
             self.wfile.write(("<p>" + control.getMessage(i) + "</p>").encode('utf-8'))

        self.wfile.write(("</td></tr></table></body></html>").encode('utf-8'))

# Read port selected by the cloud for our application
PORT = int(os.getenv('VCAP_APP_PORT', 8000))

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

