#!/bin/bash

echo -n FitIot Username:
read username

scp extractDevice.py "$username"@grenoble.iot-lab.info:
scp onBR.sh "$username"@grenoble.iot-lab.info:
scp onHost.sh "$username"@grenoble.iot-lab.info:
scp setupBR.sh "$username"@grenoble.iot-lab.info:
