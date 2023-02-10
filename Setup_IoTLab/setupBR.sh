#!/bin/bash

echo -n Username:
read username

if iotlab-auth -u "$username" | grep -q '"Written"'; then
    ID=$(iotlab-experiment submit -n riot_a8 -d 90 -l 4,archi=a8:at86rf231+site=grenoble)
    EXP="${ID//[^0-9]/}"
    iotlab-experiment wait --timeout 45 --cancel-on-timeout
    DEVSTR=$(iotlab-experiment get -d)
    DEV=`python extractDevice.py "$DEVSTR"`
    mkdir -p ~/A8/riot
    cd ~/A8/riot

    DIR="$HOME/A8/riot/RIOT"
    if [ ! -d "$DIR" ]; then
        echo Cloning RIOT repository
        git clone https://github.com/RIOT-OS/RIOT.git -b 2020.10-branch
    fi

    cd RIOT
    source /opt/riot.source
    make ETHOS_BAUDRATE=500000 DEFAULT_CHANNEL=26 BOARD=iotlab-a8-m3 -C examples/gnrc_border_router clean all
    cp examples/gnrc_border_router/bin/iotlab-a8-m3/gnrc_border_router.elf ~/A8/.
    cp ~/onBR.sh ~/A8/
    cp ~/config.conf ~/A8/

    APKDIR="$HOME/A8/riot/RIOT/examples/sensor_toCloud"
    if [ ! -d "$APKDIR" ]; then
        cp -r ~/sensor_toCloud ~/A8/riot/RIOT/examples
    fi

    DEVSSH="${DEV%%.*}"
    # use sleep since iotlab-ssh wait-for-boot not reliable
    echo Waiting 45s to make sure all nodes are up...
    sleep 45
    echo Connecting to BR with: root@node-"$DEVSSH"
    ssh root@node-"$DEVSSH"
fi
