import blescan
import sys
import requests
from datetime import datetime
import time
import bluetooth._bluetooth as bluez
import pygame
import os
import socket
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

# The default device for bluetooth scan
dev_id = 0

# Scan BLE advertisements until we see one matching our tilt uuid
def getdata():
    try:
        sock = bluez.hci_open_dev(dev_id)
    except:
        print("error accessing bluetooth device...")
        sys.exit(1)
    blescan.hci_le_set_scan_parameters(sock)
    blescan.hci_enable_le_scan(sock)
    gotData = 0
    while gotData == 0:
        returnedList = blescan.parse_events(sock, 10)
        for beacon in returnedList:
            output = beacon.split(',')
            if output[1] == green:  # Change this to the colour of your tilt
                tempf = float(output[2])
                gotData = 1
                tiltSG = float(output[3]) / 1000
                tiltTemp = int((tempf - 32) * 5.0 / 9.0)
                tiltColour = 'GREEN'
                tiltBeer = 'tdrn3iX9ucmNpbA6n'  # Change to an identifier of a particular brew
                data = {
                    'brewId': tiltBeer,
                    'temperature': tiltTemp,
                    'gravity': tiltSG
                }
                jsonObj = json.dumps(data)
                blescan.hci_disable_le_scan(sock)
                return jsonObj

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_publish(client, userdata, mid):
    print("Message Published: " + str(mid))

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.connect("mqtt.example.com", 1883, 60)  # Replace with your MQTT broker address and port
    client.loop_start()

    jsonObj = getdata()
    client.publish("tilt_data", jsonObj)

    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
    main()
