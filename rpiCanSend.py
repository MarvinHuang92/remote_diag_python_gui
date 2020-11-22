# -*- coding: UTF-8 -*-

import time
import can
 
bustype = 'socketcan_native'
channel = 'can1'
Diag_msg_id = 0x7A5

import cantestreceive as cr

def send_msg(data_str):
    valid_input = True
    try:
        data_list = data_str.split()
        byte0=len(data_list)  # the 1st byte is length
        # dlc is always 8
        if byte0 > 7:
            valid_input = False
        else:
            empty = 7 - byte0
            data = [byte0, ]
            for byte_str in data_list:
                byte_int = int(byte_str, 16)
                # byte_hex = hex(byte_int)
                # print(byte_hex)
                if not (byte_int >= 0 and byte_int <= 255):
                    valid_input = False
                    break
                data.append(byte_int)
            for i in range(empty):
                data.append(0)
    except:
        valid_input = False
    
    if valid_input:
        bus = can.interface.Bus(channel=channel, bustype=bustype, fd = True)
        msg = can.Message(arbitration_id=Diag_msg_id, dlc=8, data=data, is_fd = False, extended_id=False)
#        print(msg)
        bus.send(msg)
#        print('arbitration_id=%s, dlc=%d, data=%s\n' % (Diag_msg_id, len(data_list), str(data)))
    else:
        print('Invalid Input!')

if __name__ == "__main__":
    while True:
        data_str = input("Input Message: ")
        send_msg(data_str)

