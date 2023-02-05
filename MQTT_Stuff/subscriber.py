import csv
import json
import threading

import matplotlib.pyplot as plt
import pandas as pd
from awscrt import mqtt
from awsiot import mqtt_connection_builder


ENDPOINT = "a3kkaneczqd2o-ats.iot.us-east-1.amazonaws.com"
CLIENT_ID = "Subscriber"
PATH_TO_CERTIFICATE = "certificates/certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "certificates/private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "certificates/root.pem"

TOPIC = "test/testing"

TEMPERATURE = "temperature"
TIMESTAMP = "timestamp"
LUX = "Lux_Value"
csv_header = [TIMESTAMP, LUX]

DATAPOINTS_SHOWED = 30


# call back to trigger when a message is received
def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    payload = payload.decode("utf-8")[1:-1].replace("\\", "")
    print("Received message from topic '{}': {}".format(topic, payload))

    with open('results/results.csv', 'a') as file:
        print("Save data in results.csv ...")
        # create the csv writer
        result_writer = csv.writer(file)

        timestamp = json.loads(payload)[TIMESTAMP]
        lux = json.loads(payload)[LUX]

        # write a row to the csv file
        result_writer.writerow([timestamp, lux])

    print("Show data ...")
    # close current plot
    plt.close()

    # reading the database
    data = pd.read_csv('results/results.csv')

    plt.scatter(data[TIMESTAMP][-DATAPOINTS_SHOWED:], data[LUX][-DATAPOINTS_SHOWED:])
    plt.plot(data[TIMESTAMP][-DATAPOINTS_SHOWED:], data[LUX][-DATAPOINTS_SHOWED:])

    plt.title("Received data for topic {}\n(Last {} datapoints)".format(topic, DATAPOINTS_SHOWED))

    plt.xlabel("Timestamp")
    plt.ylabel("Lux")

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    plt.show()


print("Create CSV-file for the results ... ")
with open('results/results.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(csv_header)

print("Build connection to AWS-Endpoint {} as client {} ... ".format(ENDPOINT, CLIENT_ID))
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
print('{} is connected!'.format(CLIENT_ID))

print("Subscribe to topic {} ...".format(TOPIC))
subscribe_future, packet_id = mqtt_connection.subscribe(
    topic=TOPIC,
    qos=mqtt.QoS.AT_LEAST_ONCE,
    callback=on_message_received
)

print("Waiting for messages ...")
threading.Event().wait()
