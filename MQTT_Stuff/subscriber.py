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

SHOW_PLOT = False


def writeIn(path, payload_dict, LUX_Identifier):
    with open(path, 'a') as file:
        print("Save data in results.csv ...")
        # create the csv writer
        result_writer = csv.writer(file)

        timestamp = payload_dict[TIMESTAMP]
        lux = payload_dict[LUX_Identifier]

        # write a row to the csv file
        result_writer.writerow([timestamp, lux])


# call back to trigger when a message is received
def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    payload = payload.decode("utf-8").replace("\\", "")
    if payload[0] == "\"" and payload[-1] == "\"":
        payload = payload[1:-1]
    print("Received message from topic '{}': {}".format(topic, payload))

    payload_dict = json.loads(payload)

    if LUX + "Real" in payload_dict:
        writeIn('results/results_real.csv', payload_dict, LUX + "Real")
    elif LUX + "Fake" in payload_dict:
        writeIn('results/results_fake.csv', payload_dict, LUX + "Fake")

    if SHOW_PLOT:
        print("Show data ...")
        # close current plot
        plt.close()

        figure, axis = plt.subplots(2)
        figure.suptitle("Received data for topic {}\n(Last {} datapoints)".format(topic, DATAPOINTS_SHOWED))

        # Fake data
        fake_data = pd.read_csv('results/results_fake.csv')
        axis[0].plot(fake_data[TIMESTAMP][-DATAPOINTS_SHOWED:], fake_data[LUX][-DATAPOINTS_SHOWED:])
        axis[0].scatter(fake_data[TIMESTAMP][-DATAPOINTS_SHOWED:], fake_data[LUX][-DATAPOINTS_SHOWED:])
        axis[0].set_title("Fake data")
        axis[0].tick_params('x', labelrotation=45, labelsize="small")
        axis[0].tick_params('y', labelsize="small")

        # Real data
        real_data = pd.read_csv('results/results_real.csv')
        axis[1].plot(real_data[TIMESTAMP][-DATAPOINTS_SHOWED:], real_data[LUX][-DATAPOINTS_SHOWED:])
        axis[1].scatter(real_data[TIMESTAMP][-DATAPOINTS_SHOWED:], real_data[LUX][-DATAPOINTS_SHOWED:])
        axis[1].set_title("Real data")
        axis[1].tick_params('x', labelrotation=45, labelsize="small")
        axis[1].tick_params('y', labelsize="small")

        # Set common labels
        figure.text(0.5, 0.04, 'Timestamp', ha='center', va='center')
        figure.text(0.04, 0.5, 'Lux', ha='center', va='center', rotation='vertical')

        plt.tight_layout()
        figure.subplots_adjust(bottom=0.2, left=0.1)

        plt.show()


if __name__ == '__main__':
    print("Create CSV-files for the results ... ")
    with open('results/results_real.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(csv_header)

    with open('results/results_fake.csv', 'w') as f:
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
