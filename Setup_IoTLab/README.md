The following scripts are used in order setup Fit-IoT Lab environment of the 
project on site grenoble.
The setup includes a border router, a MQTT-SN broker (mosquitto RSMB) and the 
application sending real and fake sensor data. Before you start the setup make
sure you have cloned the whole GitHub repository to your local machine.

1. Open a terminal and run script "copyFiles.sh". This will copy all necessary
   files to your grenoble frontend. You have to provide your Fit Iot Lab 
   username.

2. Connect to grenoble site via ssh and check if all files are present by typing
   "ls". Following files and folders should be present:
	- extractDevice.py
	- onBR.sh
	- setupBR.sh
	- config.conf
	- sensor_toCloud

3. Run script "setupBR.sh". This script will:
	- setup an experiment with four A8 nodes for 90min
	- get the ID of the device which will be use as the border router
	- clone the RIOT repository if not already present
	- create binary files for the border router
	- copy the remaining files to the A8 and RIOT/examples folder in order
	  to use them on the nodes.
	- connect to the border router node via ssh

4. You should now be connected to the border router node. Run script 
   "./A8/onBR.sh". The script will flash the binaries and reset the node. It 
   will extract the IPv6 prefix and run a script in order to start the border 
   router.

5. Now you can setup the RSMB. Open a new terminal and connect to the grenoble 
   site again via ssh. Check which nodes are present by typing 
   "iotlab-experiment get -d". There should be four nodes present. The first 
   one is the border router. Connect to the second one via 
   "ssh root@node-a8-NODENUMBER.

6. Use the comman "ifconfig" in order to get the global IPv6 address of the 
   node as you will need this later on. Copy the address somewhere.

7. Run the command "broker_mqtts A8/config.conf". This will start your broker
   which listens for UDP MQTT-SN messages on port 1885 and for TCP MQTT on
   port 1886.

8. Edit the ownGateway.py file in line 27. Use the IPv6 address from step 6 
   and start the gateway with "python3 ownGateway.py".

8. Open a new terminal and connect to the grenoble frontend via ssh. And edit
   the main.c file in A8/riot/RIOT/examples/sensor_toCloud. Change the IPv6
   address in line 68 to the one you copied in step 6.

9. While in the folder build the application by using command 
   "make BOARD=iotlab-a8-m3". Copy the file to the third in the list received
   in step 5 by using command 
   "scp bin/iotlab-a8-m3/sensor_toCloud.elf root@node-a8-NODENUMBER:

10. Connect to the node with "ssh root@node-a8-NODENUMBER" and flash the 
    binary using "flash_a8_m3 sensor_toCloud.elf.

11. Use command "iotlab_reset" to restart the node and wait until you see 
    messages being received in the gateway window.
