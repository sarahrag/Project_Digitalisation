#!/bin/bash

iotlab_flash A8/gnrc_border_router.elf
iotlab_reset
cd ~/A8/riot/RIOT/dist/tools/uhcpd
make clean all
cd ../ethos
make clean all
INET6PREF=$(printenv | grep INET6_PREFIX=)
PREFIX="${INET6PREF##INET6_PREFIX=}"
./start_network.sh /dev/ttyA8_M3 tap0 "$PREFIX"::/64 500000
