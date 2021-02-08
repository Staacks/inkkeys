#These are some very specific things I do via MQTT:
#- Switching a light in my office
#- Reacting to a high CO2 level

#If you do not want to use MQTT whatsoever, you should remove it from controller.py

import paho.mqtt.client as mqtt
import json

class InkkeysMqtt:
    client = None

    server = None

    lightOn = None
    co2 = None
    debug = False

    plugTopic = "zigbee2mqtt_octopi/plug_office"
    co2Topic = "co2/data/update"

    def __init__(self, server, debug=False):
        self.debug = debug
        self.server = server
        self.client = mqtt.Client("inkkeys")

        def on_message(client, userdata, message):
            if message.topic == self.plugTopic:
                state = json.loads(str(message.payload.decode("utf-8")))
                self.lightOn = state["state"] != "OFF"
                if self.debug:
                    print("Light: " + str(self.lightOn))
            elif message.topic == self.co2Topic:
                state = json.loads(str(message.payload.decode("utf-8")))
                self.co2 = state["co2"]
                if self.debug:
                    print("CO2: " + str(self.co2))

        self.client.on_message = on_message

    def connect(self):
        if self.server == None:
            return
        self.client.connect(self.server)
        self.client.loop_start()
        self.client.subscribe(self.plugTopic)
        self.client.subscribe(self.co2Topic)
        self.client.publish(self.plugTopic + "/get",'{"state":""}')

    def disconnect(self):
        if self.server == None:
            return
        self.client.loop_stop()
        self.client.disconnect()

    def setLight(self, state):
        if self.server == None:
            return
        self.client.publish(self.plugTopic + "/set",'{"state":' + ('"ON"' if state else '"OFF"') + '}')

    def getLight(self):
        if self.server == None:
            return None
        return self.lightOn

    def getCO2(self):
        if self.server == None:
            return None
        return self.co2
