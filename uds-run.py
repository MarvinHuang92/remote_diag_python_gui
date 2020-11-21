# -*- coding: UTF-8 -*-

import time
import can
 
bustype = 'socketcan_native'
channel = 'can1'
Diag_msg_id = 0x7A5
counter = 0

def producer(freq=0.02):
    global counter
    # param id: Spam the bus with messages including the data id.
    bus = can.interface.Bus(channel=channel, bustype=bustype, fd = True)
    while True:
        msg = can.Message(arbitration_id=Diag_msg_id, dlc=8, data=[2, 0x3e, 0, 0, 0, 0, 0, 0], is_fd = True, extended_id=False)
        bus.send(msg)
        # Issue #3: Need to keep running to ensure the writing threads stay alive. ?
#        print(counter, msg)
        time.sleep(freq)
#        counter += 1

if __name__ == "__main__":
    producer(4)
