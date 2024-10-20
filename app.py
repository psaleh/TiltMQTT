from bluepy3 import btle
import sys
import json
import paho.mqtt.client as mqtt

# Assign uuid's of various colour tilt hydrometers
red    = 'a495bb10c5b14b44b5121370f02d74de'
green  = 'a495bb20c5b14b44b5121370f02d74de'
black  = 'a495bb30c5b14b44b5121370f02d74de'
purple = 'a495bb40c5b14b44b5121370f02d74de'
orange = 'a495bb50c5b14b44b5121370f02d74de'
blue   = 'a495bb60c5b14b44b5121370f02d74de'
yellow = 'a495bb70c5b14b44b5121370f02d74de'
pink   = 'a495bb80c5b14b44b5121370f02d74de'

class ScanDelegate(btle.DefaultDelegate):
    def __init__(self):
        super().__init__()

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if dev.getValueText(btle.ScanEntry.COMPLETE_LOCAL_NAME):
            if dev.addr in [green]:  # Change this to the colour of your tilt
                tempf = float(dev.rawData[4:6].hex(), 16)  # Example, might need adjustment
                tiltSG = float(dev.rawData[6:8].hex(), 16) / 1000
                tiltTemp = int((tempf - 32) * 5.0 / 9.0)
                tiltColour = 'GREEN'
                tiltBeer = 'tdrn3iX9ucmNpbA6n'  # Change to an identifier of a particular brew
                data = {
                    'brewId': tiltBeer,
                    'temperature': tiltTemp,
                    'gravity': tiltSG
                }
                jsonObj = json.dumps(data)
                client.publish("tilt_data", jsonObj)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_publish(client, userdata, mid):
    print("Message Published: " + str(mid))

def main():
    global client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.connect("mqtt.example.com", 1883, 60)  # Replace with your MQTT broker address and port
    client.loop_start()

    scanner = btle.Scanner().withDelegate(ScanDelegate())
    scanner.scan(10.0)  # Scans for 10 seconds

    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
    main()
