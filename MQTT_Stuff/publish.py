# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import json
import random
from datetime import datetime
import time

from awscrt import mqtt
from awsiot import mqtt_connection_builder

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = "a3kkaneczqd2o-ats.iot.us-east-1.amazonaws.com"
CLIENT_ID = "test_client"  # muss in aws thing -> certificates -> policies allowed sein
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

#for i in range(20):
MESSAGE = {'temperature': random.uniform(18.0, 22.0), 'timestamp': datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}
mqtt_connection.publish(
    topic=TOPIC,
    payload=json.dumps(MESSAGE),
    qos=mqtt.QoS.AT_LEAST_ONCE
)
print('Message published')
print(MESSAGE)
#time.sleep(5)

disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()
print('Disconnected')
