#!/usr/bin/env python3

import json
import subprocess
import re
import paho.mqtt.client as mqtt

# MQTT Settings
host = "IP ADDR"
username = "USER"
password = "PASS"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("ddcutilMQTT/cmnd/#")

def on_message_vol(client, userdata, msg):
    vol = msg.payload.decode('utf-8')
    if vol.isnumeric():
      if 0 <= int(vol) <= 100:
        print(str("Setting volume to"), vol)
        subprocess.call("ddcutil setvcp 62 "+vol, shell=True)
      else:
        print(str("Error"))
    else:
        match = re.search("up", vol)
        if match:
            print(str("Raising volume"))
            subprocess.call("ddcutil setvcp 62 +1", shell=True)
        else:
            match = re.search("down", vol)
            if match:
                print(str("Lowering volume"))
                subprocess.call("ddcutil setvcp 62 -1", shell=True)
            else:
                print(str("Error"))

def on_message_bri(client, userdata, msg):
    print(str("Brightness"), msg.payload.decode('utf-8'))
    bri = msg.payload.decode('utf-8')
    if bri.isnumeric():
      if 0 <= int(bri) <= 100:
        print(str("Setting brightness to"), bri)
        subprocess.call("ddcutil setvcp 10 "+bri, shell=True)
      else:
        print(str("Error"))
    else:
        match = re.search("up", bri)
        if match:
            print(str("Raising brightness"))
            subprocess.call("ddcutil setvcp 10 +1", shell=True)
        else:
            match = re.search("down", bri)
            if match:
                print(str("Lowering brightness"))
                subprocess.call("ddcutil setvcp 10 -1", shell=True)
            else:
                print(str("Error"))

def on_message_inp(client, userdata, msg):
    inp = msg.payload.decode('utf-8')
    match = re.search("HDMI1", inp)
    if match:
        print(str("Setting to HDMI1"))
        subprocess.call("ddcutil setvcp 60 05", shell=True)
    else:
        match = re.search("HDMI2", inp)
        if match:
            print(str("Setting to HDMI2/MHL"))
            subprocess.call("ddcutil setvcp 60 06", shell=True)
        else:
            match = re.search("VGA", inp)
            if match:
                print(str("Setting to VGA"))
                subprocess.call("ddcutil setvcp 60 01", shell=True)
            else:
                print(str("Error"))

client = mqtt.Client()

client.message_callback_add('ddcutilMQTT/cmnd/vol', on_message_vol)
client.message_callback_add('ddcutilMQTT/cmnd/bri', on_message_bri)
client.message_callback_add('ddcutilMQTT/cmnd/inp', on_message_inp)

client.on_connect = on_connect

client.username_pw_set(username, password)
print("Connecting...")
client.connect(host,1883,60)

client.loop_forever()