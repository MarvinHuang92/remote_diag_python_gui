# -*- coding: UTF-8 -*-

import os

def init_device():
cmd_online_1 = 'sudo ip link set can0 up type can bitrate 500000 dbitrate 2000000 restart-ms 100 berr-reporting on fd on'
cmd_online_2 = 'sudo ip link set can1 up type can bitrate 500000 dbitrate 2000000 restart-ms 100 berr-reporting on fd on'
cmd_online_3 = 'sudo ifconfig can0 txqueuelen 65536'
cmd_online_4 = 'sudo ifconfig can1 txqueuelen 65536'
os.system(cmd_online_1)
os.system(cmd_online_2)
os.system(cmd_online_3)
os.system(cmd_online_4)

if __name__ == "__main__":
    init_device()
