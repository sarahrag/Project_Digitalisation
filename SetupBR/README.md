The following scripts are used in order setup a border router on site grenoble.
In order to test the border router a host node is also setup and used to ping
any IPv6 address. Two A8 nodes are used for this.

1. Open a terminal and run script "copyFiles.sh". This will copy all necessary
   scripts to your grenoble frontend. You have to provide your Fit Iot Lab 
   username.

2. Connect to grenoble site via ssh and check if all files are present by typing
   "ls". Following files should be present:
	- extractDevice.py
	- onBR.sh
	- onHost.sh
	- setupBR.sh

3. Run script "setupBR.sh". This script will:
	- setup an experiment with two A8 nodes
	- get the device to use for the border router
	- clone the RIOT repository if not already present
	- create binary files for the border router and the host node
	- copy the remaining scripts to the A8 folder in order to use them on
	  the nodes.
	- connect to the border router node via ssh

4. You should now be connected to the border router node. Run script 
   "./A8/onBR.sh". The script will flash the binaries and reset the node. It 
   will extract the IPv6 prefix and run a script in order to start the border 
   router.

5. Now to verify that the border router is working, open a new terminal and 
   connect to the grenoble site again via ssh. Check which nodes are present by
   typing "iotlab-experiment get -d". There should be two nodes present. The
   first one is the border router. Connect to the second one via
   "ssh root@node-a8-<nodeNumber>.

6. Run the script "./A8/onHost.sh". This will flash the binaries for the host
   node, reset the node and open a miniterm connection to the M3 of the A8 node.

7. Try to ping any IPv6 address for example the Google DNS Server with
   "ping6 2001:4860:4860::8888". If you get a response, everything worked out.

