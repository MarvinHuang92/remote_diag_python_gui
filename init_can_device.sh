#!/bin/bash

sudo ip link set can0 up type can bitrate 500000 dbitrate 2000000 restart-ms 100 berr-reporting on fd on
sudo ip link set can1 up type can bitrate 500000 dbitrate 2000000 restart-ms 100 berr-reporting on fd on
 
sudo ifconfig can0 txqueuelen 65536
sudo ifconfig can1 txqueuelen 65536

sudo ip link set can0 down
sudo ip link set can1 down