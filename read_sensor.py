import ibmiotf.application
import getopt
import signal
import time
import sys
import json

class Control:
    def __init__(self):
        organization = "quickstart"
        appId = "myapp"
        authMethod = None
        authKey = None
        authToken = None
        configFilePath = None
        deviceType = "+"
        deviceId = "b0b448be6286"
        event = "+"
        self.client = None
        options = {"org": organization,
                   "id": appId,
                   "auth-method": authMethod,
                   "auth-key": authKey,
                   "auth-token": authToken}
        self.a_x = [0, 0, 0]
        self.a_y = [0, 0, 0]
        self.a_z = [0, 0, 0]
      
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
        self.client.subscribeToDeviceEvents(deviceType, deviceId, event)
        self.client.subscribeToDeviceStatus(deviceType, deviceId)

    def insertNewValue(self, a, x):
        a[0] = a[1]
        a[1] = a[2]
        a[2] = x
    
    def myEventCallback(self, event):
        json_str = json.dumps(event.data)
        data = json.loads(json_str)

        # print(data)
        # for key in ("gyro_x", "gyro_y", "gyro_z"):
        #    print(key + " = " + data["d"][key]);
        
        self.insertNewValue(self.a_x,
                            float(data["d"]["gyro_x"].replace(",", ".")))
        self.insertNewValue(self.a_y,
                            float(data["d"]["gyro_y"].replace(",", ".")))
        self.insertNewValue(self.a_z,
                            float(data["d"]["gyro_z"].replace(",", ".")))
        print(self.a_x + self.a_y + self.a_z)

    def myStatusCallback(self, status):
        print("myStatusCallback()")
        if status.action == "Disconnect":
            print(status.time.isoformat(),
                  status.device, status.action +
                  " " + status.clientAddr + " (" + status.reason + ")")
        else:
            print(status.time.isoformat(),
                  status.device, status.action + " " + status.clientAddr)
    
    def interruptHandler(self, signal, frame):
        print("interruptHandler()")
        self.client.disconnect()
        sys.exit(0)

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)
    
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    control = Control()
    signal.pause()
