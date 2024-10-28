import sys
import datetime
import time
import paho.mqtt.client as mqtt
import bluetooth._bluetooth as bluez
import json
import blescan

# Tilt Calibration Offsets
deltag = 16
deltat = -0.3

# MQTT broker details
broker = "192.168.0.14"
port = 1883
topic = "tilttest/data"
username = "hass"
password = "JtxoZ5fBJ6a5B%"

# UUIDs for various Tilt hydrometers
TILTS = {
    'a495bb10c5b14b44b5121370f02d74de': 'Red',
    'a495bb20c5b14b44b5121370f02d74de': 'Green',
    'a495bb30c5b14b44b5121370f02d74de': 'Black',
    'a495bb40c5b14b44b5121370f02d74de': 'Purple',
    'a495bb50c5b14b44b5121370f02d74de': 'Orange',
    'a495bb60c5b14b44b5121370f02d74de': 'Blue',
    'a495bb70c5b14b44b5121370f02d74de': 'Yellow',
    'a495bb80c5b14b44b5121370f02d74de': 'Pink'
}

# Ensure unique devices based on UUIDs
def distinct(objects):
    seen = set()
    unique = []
    for obj in objects:
        if obj['uuid'] not in seen:
            unique.append(obj)
            seen.add(obj['uuid'])
    return unique

# Convert Fahrenheit to Celsius
def to_celsius(fahrenheit):
    return round((fahrenheit - 32.0) / 1.8, 2)

# Monitor and log data from Tilt hydrometers
def monitor_tilt():
    while True:
        beacons = distinct(blescan.parse_events(sock, 10))
        for beacon in beacons:
            if beacon['uuid'] in TILTS.keys():
                data = {
                    'color': TILTS[beacon['uuid']],
                    'timestamp': datetime.datetime.now().isoformat(),
                    'temp': (to_celsius(beacon['major'])) + deltat,
                    'gravity': (beacon['minor']) + deltag
                }
                send_data(data)

        time.sleep(10)


#send data to MQTT broker
def send_data(data):
    client = mqtt.Client()
    client.username_pw_set(username, password)
    client.connect(broker, port, 60)
    client.loop_start()
    json_data = json.dumps(data)
    client.publish(topic, json_data)
    client.loop_stop()
    client.disconnect()
    print json_data

if __name__ == '__main__':
    dev_id = 0
    try:
        sock = bluez.hci_open_dev(dev_id)
        print 'Starting pytilt logger'
    except:
        print 'Error accessing bluetooth device...'
        sys.exit(1)

    blescan.hci_le_set_scan_parameters(sock)
    blescan.hci_enable_le_scan(sock)
    monitor_tilt()
