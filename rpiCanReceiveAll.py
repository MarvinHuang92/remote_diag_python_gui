# -*- coding: UTF-8 -*-

import can, re, time
#import re, time
#import msg_generator as mg 

# Example Format:
# Timestamp: 1605943324.306903        ID: 0112    S                DLC:  8    5e 00 00 00 40 12 1c 10     Channel: can1

'''
# Example Multi-frame:
# 10 13 62 f1 95 46 41 57
# 21 5f 44 30 42 4c 30 36
# 22 52 43 30 37 20 20 00
'''

PATTERN = r'.*Timestamp:(.*)ID:(.*)DLC:(.*)Channel:(.*)'
PATTERN_TIME = r'.*Timestamp:(.*)ID:.*'
INIT_TIME = 0
MULTI_DATA = ''
MULTI_FRAME = False
DLC_MULTI = 0
EXTRA_FRAMES = 0
PRINTED_LINES = 0

bustype = 'socketcan_native'
channel = 'can1'
Diag_msg_send_id = 0x7A5
Diag_msg_receive_id = 0x7AD
bus = can.interface.Bus(channel=channel, bustype=bustype, fd = True)

def send_uds_msg(data):
    msg = can.Message(arbitration_id=Diag_msg_send_id, dlc=8, data=data, is_fd = False, extended_id=False)
    bus.send(msg)

def format_msg(message, type='default'):
    global INIT_TIME, MULTI_DATA, MULTI_FRAME, DLC_MULTI, EXTRA_FRAMES, PRINTED_LINES
    raw_data = str(message)
#    print(raw_data)
    result = re.search(PATTERN, raw_data)
    if result:
        if type == 'default':
            # DLC and DATA
            data = result.group(3)
            data_list = data.split()
            dlc = data_list.pop(0)
            new_data_str = ''
            for byte in data_list:
                new_data_str += (' ' + str(byte).strip())
            # if 2nd frame of multi
            if MULTI_FRAME:
                # if int(data_list[0].strip(), 16) > 32:  # 32 = '20' in hex
                if EXTRA_FRAMES > 0:
                    MULTI_DATA += new_data_str[3:]
                    EXTRA_FRAMES -= 1
                    # print(EXTRA_FRAMES)
                    if EXTRA_FRAMES <= 0:
                        MULTI_FRAME = False
                else:
                    MULTI_FRAME = False
            # if the 1st frame of multi
            if not MULTI_FRAME and (data_list[0].strip() == '10'):
                MULTI_FRAME = True
                # re-define dlc as the data length of multi-frame msg
                DLC_MULTI = int(data_list[1].strip(), 16)
                EXTRA_FRAMES = (DLC_MULTI - 6) / 7
                MULTI_DATA = new_data_str[3:]
                # send msg to receive extra frames
                send_uds_msg([0x30,0,0,0,0,0,0,0])
            
            # print msg
            if not MULTI_FRAME:
                dlc_output = dlc
                data_output = new_data_str.strip()
                if not MULTI_DATA == '':
                    dlc_output = DLC_MULTI
                    data_output = MULTI_DATA.strip()
                    MULTI_DATA = ''
                    DLC_MULTI = 0
                # TIMESTAMP
                timestamp = float(result.group(1).strip()) - INIT_TIME
                # ID
                id_str = result.group(2).strip()[0:4].lstrip('0')
                # Channel
                channel_str = result.group(4).strip()
                # skip printing the UDS session-keep msg
                if not data_output[0:5] == '02 7e':
                    print('%6.4f\t%s\t%s\t%s\t\t\t%s' % (timestamp, id_str, dlc_output, data_output, channel_str))
                    PRINTED_LINES += 1

        elif type == 'timestamp':
            timestamp = result.group(1).strip()
            INIT_TIME = float(timestamp)
    else:
        print('Invalid Message Format!')
        PRINTED_LINES += 1
#    return raw_data

def print_headers():
    print('TIME \tID \tDLC \tDATA \t\t\tChannel')

if __name__ == "__main__":
    print_headers()

    # get init timestamp
    message = bus.recv(1.0) # Timeout in seconds.
    if not message is None:
        format_msg(message, type='timestamp')
    #    print(INIT_TIME)
    #    print('')

    last_time = time.time()
    while True:
        if PRINTED_LINES >= 10:
            print('')
            print_headers()
            PRINTED_LINES = 0
        
        message = bus.recv(1.0) # Timeout in seconds.
    #    message = mg.generate_can_msg(31)
        
        if message is None:
            print('Timeout occurred, no message.')
            PRINTED_LINES += 1
        else:
#        elif message.arbitration_id == Diag_msg_receive_id:
            format_msg(message)
            
        # send msg to keep in non-default session
        current_time = time.time()
        if current_time - last_time >= 4:
            last_time = current_time
            send_uds_msg([0x2,0x3e,0,0,0,0,0,0])
        
