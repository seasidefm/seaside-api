import json
import os
import certifi

import paho.mqtt.client as mqtt

topics = {
    "NEW_HEAT": "new-heat",
    "UPDATE_HEAT": "update-heat",
}


def get_mqtt_client():
    if not os.environ.get('MQTT_HOST'):
        print('WARNING: CANNOT FIND MQTT HOST IN ENV')

    mqtt_user = os.environ.get('MQTT_USER')
    mqtt_pwd = os.environ.get('MQTT_PWD')
    if not mqtt_user or not mqtt_pwd:
        print('WARNING: No mqtt user or password set, defaulting to empty string!')

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(_, userdata, flags, rc):
        print("Seaside API is connected to to MQTT broker with code: " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        # client.subscribe(topic)

    def on_fail(_):
        print("Unable to connect to mqtt broker! Please check your user and password, as well as TLS and port")

    client = mqtt.Client("seaside-api", transport="tcp")
    client.username_pw_set(mqtt_user, mqtt_pwd)
    client.tls_set(certifi.where())
    client.tls_insecure_set(True)
    client.on_connect = on_connect
    client.on_connect_fail = on_fail

    return client


class MqttService:
    def __init__(self):
        self.client = get_mqtt_client()

    @staticmethod
    def format_heat_message(heat: int):
        if heat == 0:
            return "heat level rising"
        else:
            return f"heat level: {heat}"

    def set_heat_level(self, message: dict):
        print('Sending heat level message')
        c = self.client
        c.connect(os.environ['MQTT_HOST'], 8883, 60)
        c.publish(topic=topics['UPDATE_HEAT'], payload=json.dumps(message))
        c.disconnect()
