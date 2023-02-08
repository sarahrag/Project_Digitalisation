# Project Digitalisation: IoT - From the Microcontroller to the Cloud

## Requirements

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
