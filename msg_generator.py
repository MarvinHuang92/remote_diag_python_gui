# -*- coding: UTF-8 -*-

import time, random

starting_time = time.time()

dlc_list = [0, 1, 2, 3, 4, 5, 6, 7,
       8, 8, 8,12,12,12,16,16,
      16,20,20,20,24,24,24,32,
      32,32,48,48,48,64,64,64]

def hex_to_str(integer):
    s = str(hex(integer)).upper()
    if len(s) == 3:
        s = s[0:2] + '0' + s[-1]
    # s = '0x' + s[2:4]
    s = s[2:4]
    return s

def generate_can_msg(max_id):
    id = random.randint(0, max_id)
    timestamp = time.time() - starting_time
    dlc = dlc_list[id]
    type = "CAN"
    if dlc > 8:
        type = "CAN_FD"
    channel = 'CAN' + str(random.randint(1, 4))
    data = ''
    for i in range(dlc):
        # cannot display too long
        if i <= 24:
            raw_data = hex_to_str(random.randint(0, 255))
            data += (' ' + raw_data)
        else:
            data += ' ...'
            break
    data = data.strip()
    id_str = hex_to_str(id)
    
    # original output
    # output = 'Time: %8.3f\tID: %s\tData_Length: %d\tType: %s\tChannel: %s\tData: %s' %(timestamp, id_str, dlc, type, channel, data)
    # output of Rapsberrypi format
    output = 'Time: %8.3f\tID: %s\tDLC: %d\t%s\tChannel: %s\tType: %s' %(timestamp, id_str, dlc, data, channel, type)
    return output

if __name__ == "__main__":
    while True:
        message = generate_can_msg(31)
        print(message)
        time.sleep(0.2)

