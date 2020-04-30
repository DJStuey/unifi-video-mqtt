#!/usr/bin/python3

import os
import time
import paho.mqtt.client as mqtt
import logging

MQTT_BASE_TOPIC = 'camera/motion'
MQTT_BROKER = "192.168.x.x"
LOGPATH = "/var/log/unifi-video/motion.log"
MQTT_PORT = 1883

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# client.connect(MQTT_BROKER, 1883, 60)

def follow(filename):
    f = open(filename, 'r')
    f.seek(0, os.SEEK_END)

    while True:
        line = f.readline()
        if not line:
            time.sleep(0.1)
            continue    #retry
        yield line      #Emit a line

for line in follow(LOGPATH):
    row = line.split(' ')
    details = row[8].split('|')
    CAMNAME = details[1].strip('[]')
    if CAMNAME == "Front":
        CAMNAME = "Front_Porch"
    CAMID = details[0].strip('[]')

    if CAMNAME == "Front_Porch":
        status = (row[11].split(':'))[1]
    else:
        status = (row[10].split(':'))[1]

    if status.strip() == 'start':
        state = "ON"
    else:
        state = "OFF"
    client.connect(MQTT_BROKER, MQTT_PORT, 10)
    client.publish(MQTT_BASE_TOPIC + "/" + CAMNAME, state)
    print('Motion ' + status + " on " + CAMNAME + ".")

