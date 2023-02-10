Subscribe to the AWS Endpoint to save and visualize the data from MQTT messages

The Python file `subscribe.py` connects to the AWS IoT Core Endpoint and the topic, both specified in the file itself.

AWS IoT Core use authentication over TLS, therefore you need the certificate, the private and public key and the root CA
for AWS IoT. You have to add these to the certificates folder, with the following file names:

- `certificate.pem.crt`
- `private.pem.key`
- `public.pem.key`
- `root.pem`

To start the subscriber you have to start a development environment like PyCharm and run code there. If you want to run
it in a terminal, the plotting has to be disabled, by setting `SHOW_PLOT` in line 25 to `False`. After that you can also run:

`python3 subscriber.py`

After that the connection to AWS IoT Core is estamlished and the programm is waiting for messages. When receiving a MQTT
message, it is extracted, saved in the `results.csv` file and the last N datapoints are visualized in a diagram.

The program is suitable for Python 3.9 and the following python libraries are used:

- csv
- json
- threading
- matplotlib.pyplot
- pandas
- awscrt.mqtt
- awsiot.mqtt_connection_builder

