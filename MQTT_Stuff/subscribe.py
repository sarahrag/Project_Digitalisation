import json
import threading

from awscrt import mqtt
from awsiot import mqtt_connection_builder

import csv

import pandas as pd
import matplotlib.pyplot as plt

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = "a3kkaneczqd2o-ats.iot.us-east-1.amazonaws.com"
CLIENT_ID = "test_client"  # muss in thing -> certificates -> policies allowed sein
PATH_TO_CERTIFICATE = "certificates/certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "certificates/private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "certificates/root.pem"
TOPIC = "test/testing"

csv_header = ['timestamp', 'temperature']

# call back to trigger when a message is received
def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    print("Received message from topic '{}': {}".format(topic, payload))

    with open('results/results.csv', 'a') as f:
        # create the csv writer
        writer = csv.writer(f)

        timestamp = json.loads(payload)["timestamp"]
        temperature = json.loads(payload)["temperature"]

        # write a row to the csv file
        writer.writerow([timestamp, temperature])

    '''plt.close()

    # reading the database
    data = pd.read_csv('results/results.csv')

    plt.scatter(data['timestamp'], data['temperature'])

    plt.title("Test")

    plt.xlabel('Timestamp')
    plt.ylabel('Temperature')

    plt.show()'''


with open('results/results.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(csv_header)

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

subscribe_future, packet_id = mqtt_connection.subscribe(
    topic=TOPIC,
    qos=mqtt.QoS.AT_LEAST_ONCE,
    callback=on_message_received
)

threading.Event().wait()
