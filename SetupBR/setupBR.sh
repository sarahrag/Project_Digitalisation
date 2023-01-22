#!/bin/bash

echo -n Username:
read username

if iotlab-auth -u "$username" | grep -q '"Written"'; then
    ID=$(iotlab-experiment submit -n riot_a8 -d 45 -l 2,archi=a8:at86rf231+site=grenoble)
    EXP="${ID//[^0-9]/}"
    iotlab-experiment wait --timeout 45 --cancel-on-timeout
    DEVSTR=$(iotlab-experiment get -d)
    DEV=`python extractDevice.py "$DEVSTR"`
    mkdir -p ~/A8/riot
    cd ~/A8/riot
    DIR="~/A8/riot/RIOT"
    if [ ! -d "$DIR" ]; then
        git clone https://github.com/RIOT-OS/RIOT.git -b 2020.10-branch
    fi
    cd RIOT
    source /opt/riot.source
    make ETHOS_BAUDRATE=500000 DEFAULT_CHANNEL=26 BOARD=iotlab-a8-m3 -C examples/gnrc_border_router clean all
    cp examples/gnrc_border_router/bin/iotlab-a8-m3/gnrc_border_router.elf ~/A8/.
    # build for other node ...
    make DEFAULT_CHANNEL=26 BOARD=iotlab-a8-m3 -C examples/gnrc_networking clean all
    cp examples/gnrc_networking/bin/iotlab-a8-m3/gnrc_networking.elf ~/A8/
    # copy scripts for nodes to A8 folder
    cp ~/onBR.sh ~/A8/.
    cp ~/onHost.sh ~/A8/
    # connect to BR
    DEVSSH="${DEV%%.*}"
    echo Connecting to BR with: root@node-"$DEVSSH"
    ssh root@node-"$DEVSSH"
fi
