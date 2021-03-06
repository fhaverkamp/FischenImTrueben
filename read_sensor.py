import ibmiotf.application
import getopt
import signal
import time
import sys
import json

class Control:
    def __init__(self, deviceType, deviceId, options):
        self.client = None
        self.messages = []
        self.event = "+"

        try:
            self.client = ibmiotf.application.Client(options)
            self.client.connect()
        except ibmiotf.ConfigurationException as e:
            print(str(e))
            sys.exit()
        except ibmiotf.UnsupportedAuthenticationMethod as e:
            print(str(e))
            sys.exit()
        except ibmiotf.ConnectionException as e:
            print(str(e))
            sys.exit()

        self.client.deviceEventCallback = self.myEventCallback
        self.client.deviceStatusCallback = self.myStatusCallback
        self.client.subscribeToDeviceEvents(deviceType, deviceId, self.event)
        self.client.subscribeToDeviceStatus(deviceType, deviceId)

    def myEventCallback(self, event):
        json_str = json.dumps(event.data)
        data = json.loads(json_str)

        if (len(self.messages) == 10):
            self.messages.pop()

        self.messages.insert(0, data)

        print("Last 10 messages (if there are any ...)")
        for d in (self.messages):
            print("  " + str(d))

        #print("plain json data:")
        #print(data)
        #print("parsed data:")
        #for key in ("myName", "cputemp", "cpuload", "sine", "outsidetemp0",
        #            "outsidetemp1", "distance"):
        #    print("  " + key + " = " + str(data["d"][key]));


    def myStatusCallback(self, status):
        if status.action == "Disconnect":
            print(status.time.isoformat(),
                  status.device, status.action +
                  " " + status.clientAddr + " (" + status.reason + ")")
        else:
            print(status.time.isoformat(),
                  status.device, status.action + " " + status.clientAddr)

    def getMessage(self, no):
        return self.messages[no]

    def getMaxMessage(self):
        return len(self.messages)

    def interruptHandler(self, signal, frame):
        print("interruptHandler()")
        self.client.disconnect()
        sys.exit(0)

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

devices = [
    { "deviceType": "raspberrypi",
      "deviceId": "b827eb8d5add",
      "options": { "org": "4r4gwj",
                   "id": "iotf-service",
                   "auth-method": "apikey",
                   "auth-key": "a-4r4gwj-puvtgsvb4w",
                   "auth-token": "D_AHixjQsbQvg4EDnb" }
      },
    { "deviceType": "raspberrypi",
      "deviceId": "b827ebc0f49b",
      "options": { "org": "4r4gwj",
                   "id": "iotf-service",
                   "auth-method": "apikey",
                   "auth-key": "a-4r4gwj-puvtgsvb4w",
                   "auth-token": "D_AHixjQsbQvg4EDnb" }
      },
    ]

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    device = devices[0]
    control = Control(device["deviceType"], device["deviceId"], device["options"])
    signal.pause()
