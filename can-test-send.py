# -*- coding: UTF-8 -*-

import time
# import can
 
bustype = 'socketcan_native'
channel = 'can1'
Diag_msg_id = '0x7AE'

'''
def producer(id):
    # param id: Spam the bus with messages including the data id.
    bus = can.interface.Bus(channel=channel, bustype=bustype, fd = True)
    while True:
        for i in range(100):
            msg = can.Message(arbitration_id=0x06E, dlc=15, data=[id, 0, 0, 1, 3, 1, 4, i, i, i, i, i], is_fd = True, extended_id=False)
            bus.send(msg)
            # Issue #3: Need to keep running to ensure the writing threads stay alive. ?
            time.sleep(0.2)
        print('Running...')
        time.sleep(1)
'''

def send_msg(data_str):
    valid_input = True
    try:
        data_list = data_str.split()
        data = []
        for byte_str in data_list:
            byte_int = int(byte_str, 16)
            # byte_hex = hex(byte_int)
            # print(byte_hex)
            if not (byte_int >= 0 and byte_int <= 255):
                valid_input = False
                break
            data.append(byte_int)
    except:
        valid_input = False
    
    if valid_input:
        # bus = can.interface.Bus(channel=channel, bustype=bustype, fd = True)
        # msg = can.Message(arbitration_id=Diag_msg_id, dlc=len(data_list), data=data, is_fd = True, extended_id=False)
        # bus.send(msg)
        print('arbitration_id=%s, dlc=%d, data=%s\n' % (Diag_msg_id, len(data_list), str(data)))
    else:
        print('Invalid Input!')

while True:
    data_str = input("Input Message: ")
    send_msg(data_str)



# producer(1)
