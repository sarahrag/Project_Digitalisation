'''
Test publisher for MQTT messages to AWS IoT Core MQTT Broker. Not in productive use for the project.
'''

import json
import random
import time
from datetime import datetime

from awscrt import mqtt
from awsiot import mqtt_connection_builder


ENDPOINT = "a3kkaneczqd2o-ats.iot.us-east-1.amazonaws.com"
CLIENT_ID = "testclient"
PATH_TO_CERTIFICATE = "certificates/certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "certificates/private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "certificates/root.pem"
TOPIC = "test/testing"

mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=ENDPOINT,
    cert_filepath=PATH_TO_CERTIFICATE,
    pri_key_filepath=PATH_TO_PRIVATE_KEY,
    ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
    client_id=CLIENT_ID
)

connect_future = mqtt_connection.connect()

# result() waits until a result is available
connect_future.result()
print(f'{CLIENT_ID} is connected!')

for i in range(20):
    MESSAGE = {"Lux_ValueFake": random.uniform(19.0, 21.0), "timestamp": datetime.now().strftime("%H:%M:%S")}
    mqtt_connection.publish(
        topic=TOPIC,
        payload=str(json.dumps(MESSAGE)),
        qos=mqtt.QoS.AT_LEAST_ONCE
    )
    print('Message published')
    print(json.dumps(MESSAGE))
    time.sleep(1)

    MESSAGE = {"Lux_ValueReal": random.uniform(19.0, 21.0), "timestamp": datetime.now().strftime("%H:%M:%S")}
    mqtt_connection.publish(
        topic=TOPIC,
        payload=str(json.dumps(MESSAGE)),
        qos=mqtt.QoS.AT_LEAST_ONCE
    )
    print('Message published')
    print(json.dumps(MESSAGE))
    time.sleep(1)



disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()
print('Disconnected')
