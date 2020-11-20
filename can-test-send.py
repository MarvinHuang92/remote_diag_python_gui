import time
import can
 
bustype = 'socketcan_native'
channel = 'can1'
 
def producer(id):
    """:param id: Spam the bus with messages including the data id."""
    bus = can.interface.Bus(channel=channel, bustype=bustype, fd = True)
    while True:
        for i in range(100):
            msg = can.Message(arbitration_id=0x06E, dlc=13, data=[id, i, 0, 1, 3, 1, 4, 1, i, i, i, i], is_fd = True, extended_id=False)
            bus.send(msg)
        # Issue #3: Need to keep running to ensure the writing threads stay alive. ?
            time.sleep(0.2)
        print('Running...')
        time.sleep(1)
 
producer(99)