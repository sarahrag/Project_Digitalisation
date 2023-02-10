#!/bin/bash

echo -n FitIot Username:
read username

scp onBR.sh "$username"@grenoble.iot-lab.info:
scp setupBR.sh "$username"@grenoble.iot-lab.info:
scp config.conf "$username"@grenoble.iot-lab.info:
scp extractDevice.py "$username"@grenoble.iot-lab.info:
scp -r sensor_toCloud "$username"@grenoble.iot-lab.info:
