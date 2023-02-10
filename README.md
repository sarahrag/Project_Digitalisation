# Project Digitalisation: IoT - From the Microcontroller to the Cloud

The objective of this project is to send data from an embedded sensor to a cloud service provided bei Amazon Web Services (AWS). The microcontrollers which are used in this tutorial are provided by [FIT IoT-LAB](https://www.iot-lab.info/).

## Prerequisites
In order to be able to reproduce this tutorial, you need an AWS account as well as an account for FIT IoT-LAB. Furthermore, it is highly recommended to reproduce the tutorial within a Linux based environment, since it was developed in Ubuntu version 22.04.

## Project architecture
The project architecture is as follows:
![IoT-Project-Planned drawio-3](https://user-images.githubusercontent.com/49904886/217534647-0d5993a8-e2fb-4f08-be31-62cb66850bf4.png)

## Project Setup

### AWS IoT Core Setup
In this Project the AWS IoT Core MQTT Broker is used, so it has to be setted up as following:

1. In AWS IoT Core create a Thing
    1. Under *Manage -> Things* select "Create thing"
    2. Enter a name and leave the other fields as they are
    3. On "Attach policies to certificate" create a new policy
    4. Name the policy and for simplification add a policy document that allows all policy actions (\*) for all policy rescources (\*) 
    5. Attacht the policy to the thing and finish the creation
    6. Download the certificates and keys (Device certificate, public and private key, root CA) 
    7. To ensure a smooth process rename the downloaded certificates and keys to:
     * `certificate.pem.crt` (Device certificate)
     * `private.pem.key` (Private key)
     * `public.pem.key` (Public key)
     * `root.pem` (Root CA)
2. Under *Settings -> Device* data endpoint in AWS IoT Core the endpoint that is used for MQTT Clients is located. Copy the endpoint, because it has to be pasted in some files

### Setup FIT IoT-LAB environment
The first part of the project is the setup of the FIT IoT-LAB environment, including the border router, the mosquitto "Really Small Message Broker" (RSMB), the application to send real and fake sensor data with the MQTT-SN Client and the selfmade gateway.
For this part follow the instructions in the Readme.md in [Setup IoT Lab](https://github.com/sarahrag/Project_Digitalisation/tree/main/Setup_IoTLab)

### Setup subscriber
The second part of the project is the subscribing MQTT Client to receive the send data directly from AWS IoT Core, save them and (optionally) visualize them.
For this part follow the instructions in the Readme.md in [Subscriber](https://github.com/sarahrag/Project_Digitalisation/tree/main/MQTT_Stuff)
