The following scripts are used in order setup Fit-IoT Lab environment of the 
project on site grenoble.
The setup includes a border router, a MQTT-SN broker (mosquitto RSMB) and the 
application sending real and fake sensor data. Before you start the setup make
sure you have cloned the whole GitHub repository to your local machine.

1. Open a terminal and run script `./copyFiles.sh`. This will copy all necessary
   files to your grenoble frontend. You have to provide your Fit Iot Lab 
   username.

2. Connect to grenoble site via ssh with `<username>@grenoble.iot-lab.info`and 
   check if all files are present by typing `ls`. Following files and folders 
   should be present:
	- extractDevice.py
	- onBR.sh
	- setupBR.sh
	- config.conf
	- sensor_toCloud

3. Run script `./setupBR.sh`. After you enter you IoT Lab credentials th script will:
	- setup an experiment with four A8 nodes for 90min (only need three, one for backup)
	- get the ID of the device which will be use as the border router
	- clone the RIOT repository if not already present
	- create binary files for the border router
	- copy the remaining files to the A8 and RIOT/examples folder in order
	  to use them on the nodes.
	- connect to the border router node via ssh

4. You should now be connected to the border router node. Run script 
   `./A8/onBR.sh`. The script will flash the binaries and reset the node. It 
   will extract the IPv6 prefix and run a script in order to start the border 
   router. After it is done your terminal output should look like this:
   ```
   cc -O3 -Wall ethos.c -o ethos
   net.ipv6.conf.tap0.forwarding = 1
   net.ipv6.conf.tap0.accept_ra = 0
   ----> ethos: sending hello.
   ----> ethos: activating serial pass through.
   ----> ethos: hello reply received
   ----> ethos: hello reply received
   ```
   
5. Now you can setup the RSMB. Open a new terminal and connect to the grenoble 
   site again via ssh. Check which nodes are present by typing `iotlab-experiment get -d`.
   There should be four nodes present.
   ```
   {
    "0": [
        "a8-103.grenoble.iot-lab.info",
        "a8-104.grenoble.iot-lab.info",
        "a8-105.grenoble.iot-lab.info",
        "a8-106.grenoble.iot-lab.info"
    ]
   }
   ```
   The first one is the border router. Connect to the second one via 
   `ssh root@node-a8-NODENUMBER`.

6. Use the comman "ifconfig" in order to get the global IPv6 address of the 
   node as you will need this later on. Copy the address somewhere. It should
   look like this:
   `inet6 addr: 2001:660:5307:3000::68/64 Scope:Global`

7. Run the command "broker_mqtts A8/config.conf". This will start your broker
   which listens for UDP MQTT-SN messages on port 1885 and for TCP MQTT on
   port 1886.
   ```
   root@node-a8-104:~# broker_mqtts A8/config.conf 
   20230208 210934.062 CWNAN9999I Really Small Message Broker
   20230208 210934.067 CWNAN9998I Part of Project Mosquitto in Eclipse
   (http://projects.eclipse.org/projects/technology.mosquitto)
   20230208 210934.069 CWNAN0049I Configuration file name is A8/config.conf
   20230208 210934.076 CWNAN0053I Version 1.3.0.2, Dec 20 2020 23:34:33
   20230208 210934.077 CWNAN0054I Features included: bridge MQTTS 
   20230208 210934.078 CWNAN9993I Authors: Ian Craggs (icraggs@uk.ibm.com), Nicholas O'Leary
   20230208 210934.083 CWNAN0300I MQTT-S protocol starting, listening on port 1885
   20230208 210934.085 CWNAN0014I MQTT protocol starting, listening on port 1886
   ```
   
8. Edit line 27 in the ownGateway.py file on your local machine to use the IPv6 address from 
   step 6. Also make sure to provide your personal AWS IoT Core credentials and the path to 
   the certificate files on your machine. Start the gateway with `python3 ownGateway.py`. 
   On the terminal where your RSMB runs the output should now like like this:
   ```
   20230208 211328.649 5 gateway <- CONNECT
   20230208 211328.651 CWNAN0033I Connection attempt to listener 1886 received from client 
   gateway on address 2a02:908:111:2420:10ee:a7f9:8cc8:14e:36718
   20230208 211328.652 5 gateway -> CONNACK rc: 0 (0)
   20230208 211328.682 5 gateway <- SUBSCRIBE msgid: 1
   20230208 211328.683 5 gateway -> SUBACK msgid: 1 (0)
   ```
   while the output of the terminal where the gateway script runs looks like this:
    
   ```
   sys.version_info(major=3, minor=10, micro=6, releaselevel='final', serial=0)
   test_client is connected!
   connecting to broker  2001:660:5307:3000::68
   subscribing to  sensorData
   ```

9. Open a new terminal and connect to the grenoble frontend via ssh. And edit
   the main.c file in A8/riot/RIOT/examples/sensor_toCloud. Change the IPv6
   address in line 68 to the one you copied in step 6.
   `ipv6_addr_from_str((ipv6_addr_t *)&gw.addr.ipv6, "2001:660:5307:3000::68");`

10. While in the folder run command `source /opt/riot.source` and build the application
   command `make BOARD=iotlab-a8-m3`. Copy the file to the third in the list received 
   in step 5 by using command:
   ```
   scp bin/iotlab-a8-m3/sensor_toCloud.elf root@node-a8-NODENUMBER:
   `

11. Connect to the node with `ssh root@node-a8-NODENUMBER` and flash the 
    binary using `flash_a8_m3 sensor_toCloud.elf`.

12. Use command `iotlab_reset` to restart the node and wait a bit until you see 
    messages being received in the gateway window as shown below. You should also
    see traffic going through the RSMB.
    ```
    received message = {"Lux_ValueFake": 29.10,  "timestamp": "00:00:18"}
    received message = {"AccelY": -300, "timestamp": "00:00:18"}
    received message = {"Lux_ValueFake": 30.73,  "timestamp": "00:00:20"}
    received message = {"AccelY": -300, "timestamp": "00:00:20"}
    received message = {"Lux_ValueFake": 30.57,  "timestamp": "00:00:22"}
    received message = {"AccelY": -300, "timestamp": "00:00:22"}
    received message = {"Lux_ValueFake": 28.98,  "timestamp": "00:00:23"}
    received message = {"AccelY": -308, "timestamp": "00:00:23"}
    ```
    
Congratulations, you are now sending fake and real data to you AWS IoT core instance!
