#!/bin/bash

iotlab_flash A8/gnrc_networking.elf
iotlab_reset
miniterm.py /dev/ttyA8_M3 500000
