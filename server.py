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

        print("Sending some html data now ... " + self.path)

        if (self.path is not "/"):
            return Handler.do_GET(self)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(("<html>\n" +
                          "<head>" +
                          "  <title>Fischen im Trueben</title>" +
                          "  <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">" +
                          "  <meta http-equiv=\"refresh\" CONTENT=\"3\">\n" +
                          "  <link rel=\"stylesheet\" href=\"stylesheets/style.css\"/>\n" +
                          "</head>\n" +
                          "<body>\n" +
                          "  <table>\n" +
                          "    <tr>\n" +
                          "      <td style='width: 30%;'>\n" +
                          "        <img class='newappIcon' src='images/newapp-icon.png'></td>\n" +
                          "      <td>\n" +
                          "        <h1 id=\"message\">Fischen im Trueben</h1></td>\n" +
                          "      <td>\n" +
                          "        Displaying the Sensor data of my RaspberryPI 3.</td>\n" +
                          "    </tr>\n" +
                          "  </table>\n").encode('utf-8'))

        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        self.wfile.write(("  <table>\n").encode('utf-8'))

        sensor_table = self.SensorToHTML()

        self.wfile.write(sensor_table.encode('utf-8'))
        self.wfile.write(("  </table>\n" +
                          "</body>\n" +
                          "</html>\n").encode('utf-8'))

    def SensorToHTML(self):
        # Print table header
        table = "    <tr style=\"font-weight:bold\">"
        for key in ("myName", "cputemp", "cpuload", "sine", "outsidetemp0",
                    "outsidetemp1", "distance"):
            table = table + "<td>" + key + "</td>"
        table = table + "</tr>\n"

        for i in range(0, control[0].getMaxMessage()):
            data = control[0].getMessage(i)

            print(data)

            table = table + "    <tr>"
            for key in ("myName", "cputemp", "cpuload", "sine", "outsidetemp0",
                        "outsidetemp1", "distance"):
                if (data['d'].get(key) != None):
                    table = table + "<td>" + str(data['d'][key]) + "</td>"
            table = table + "</tr>\n"

        return table

# Read port selected by the cloud for our application
PORT = int(os.getenv('VCAP_APP_PORT', 8000))

# Change current directory to avoid exposure of control files
os.chdir('static')

# Application
# API-Schluessel a-4r4gwj-kdcdgxusom
# Authentifizierungstoken t6yj+C(Uop0ThD8Bag
#
# RaspberryPI1
# Organisations-ID 4r4gwj
# Geraetetyp raspberrypi
# Geraete-ID b827ebc0f49b
# Authentifizierungsmethode token
# Authentifizierungstoken _PYgtFq3tnhM2hG5f?

# RaspberryPI1
# Organisations-ID 4r4gwj
# Geraetetyp raspberrypi
# Geraete-ID b827eb8d5add
# Authentifizierungsmethode token
# Authentifizierungstoken V?FC+pX@noKIReViPJ

devices = [
    { "deviceType": "raspberrypi",
      "deviceId": "b827eb8d5add",
      "options": { "org": "4r4gwj",
                   "id": "iotf-service",
                   "auth-method": "apikey",
                   "auth-key": "a-4r4gwj-puvtgsvb4w",
                   "auth-token": "D_AHixjQsbQvg4EDnb" }
      },
#    { "deviceType": "raspberrypi",
#      "deviceId": "b827ebc0f49b",
#      "options": { "org": "4r4gwj",
#                   "id": "iotf-service",
#                   "auth-method": "apikey",
#                   "auth-key": "a-4r4gwj-puvtgsvb4w",
#                   "auth-token": "D_AHixjQsbQvg4EDnb" }
#      },
    ]

control = []

for device in devices:
    print("Adding: " + str(device))
    c = Control(device["deviceType"], device["deviceId"], device["options"])
    control.append(c)

httpd = Server(("", PORT), MyHandler)
try:
    print("Start serving at port %i" % PORT)
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()
