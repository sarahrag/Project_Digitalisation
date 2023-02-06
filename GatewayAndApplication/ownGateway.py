#! c:\python34\python3
#!/usr/bin/env python
##demo code provided by Steve Cope at www.steves-internet-guide.com
##email steve@steves-internet-guide.com
##Free to use for any purpose
##If you like and use this code you can
##buy me a drink here https://www.paypal.me/StepenCope
import signal
import queue
import time
import sys
import paho.mqtt.client as paho
import json
import random
from datetime import datetime
import time

from awscrt import mqtt
from awsiot import mqtt_connection_builder

print(sys.version_info)

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = "a3kkaneczqd2o-ats.iot.us-east-1.amazonaws.com"
CLIENT_ID = "test_client"  # muss in aws thing -> certificates -> policies allowed sein
PATH_TO_CERTIFICATE = "certificates/certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "certificates/private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "certificates/root.pem"
TOPIC = "test/testing"

broker="2001:660:5307:3000::68" # this is the RSMB
message_q=queue.Queue()
#handles abort from keyboard
def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught...".format(signal))
    exit(0)
signal.signal(signal.SIGINT, keyboardInterruptHandler)

def empty_queue(delay=0):
    while not message_q.empty():
      m=message_q.get()
      print("Received message  ",m)
    if delay!=0:
      time.sleep(delay)
#define callback
def on_message(client, userdata, message):
   time.sleep(1)
   print("received message =",str(message.payload.decode("utf-8")))
   # publish message to aws
   MESSAGE = str(message.payload.decode("utf-8"))
   mqtt_connection.publish(
   topic=TOPIC,
   payload=json.dumps(MESSAGE),
   qos=mqtt.QoS.AT_LEAST_ONCE
)


# ---------- connect to aws
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
# ---------- connect to aws

client= paho.Client("gateway")  #create client object client1.on_publish = on_publish                          #assign function to callback client1.connect(broker,port)                                 #establish connection client1.publish("house/bulb1","on")
######
#client.connect("mqtt.eclipseprojects.io",1883, 60)

#####
topic1="mqttsn-test"
topic2="sensorData"
print("connecting to broker ",broker)
client.connect(broker, 1886)#connect
print("subscribing to ",topic2)
client.subscribe(topic2)#subscribe
client.on_message=on_message
client.loop_start() #start loop to process received messages

#time.sleep(3)

try:
  while True:
    time.sleep(1)
    empty_queue(0)
    pass
except KeyboardInterrupt:
    print ("You hit control-c")


time.sleep(1)


client.disconnect() #disconnect
client.loop_stop() #stop loop

