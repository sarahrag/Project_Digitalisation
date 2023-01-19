import json
import ssl

import paho.mqtt.client as mqtt

AWS_ENDPOINT = "a3kkaneczqd2o-ats.iot.us-east-1.amazonaws.com"
AWS_CLIENT_ID = "test_client"  # muss in thing -> certificates -> policies allowed sein
AWS_PATH_TO_CERTIFICATE = "certificates/certificate.pem.crt"
AWS_PATH_TO_PRIVATE_KEY = "certificates/private.pem.key"
AWS_PATH_TO_AMAZON_ROOT_CA_1 = "certificates/root.pem"
AWS_TOPIC = "test/testing"


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg['topic'] + " " + str(msg['payload']))
    client.publish(AWS_TOPIC, json.dumps({"message": str(msg['payload'])}), qos=1)


client = mqtt.Client(AWS_CLIENT_ID)
client.on_connect = on_connect
client.on_message = on_message

client.tls_set(AWS_PATH_TO_AMAZON_ROOT_CA_1,
               certfile=AWS_PATH_TO_CERTIFICATE,
               keyfile=AWS_PATH_TO_PRIVATE_KEY,
               cert_reqs=ssl.CERT_REQUIRED,
               tls_version=ssl.PROTOCOL_TLSv1_2,
               ciphers=None)

client.connect(AWS_ENDPOINT, 8883, 60)

#on_message(client, None, {'topic': AWS_TOPIC, 'payload': 'Halloooo'})

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
