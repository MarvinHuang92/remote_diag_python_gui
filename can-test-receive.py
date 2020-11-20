# -*- coding: UTF-8 -*-

# import can, re, time
import re, time
import msg_generator as mg 

PATTERN = r'.*DLC:(.*)Channel.*'
can_interface = 'can1'
# bus = can.interface.Bus(can_interface, bustype='socketcan_native', fd = True)
while True:
    # message = bus.recv(5.0) # Timeout in seconds.
    message = mg.generate_can_msg(31)
    time.sleep(0.2)
    
    if message is None:
        print('Timeout occurred, no message.')
    else:
        raw_data = str(message)
        print(raw_data)
        result = re.search(PATTERN, raw_data)
        if result:
            data = result.group(1)
            data_list = data.split()
            dlc = data_list.pop(0)
            new_data_str = ''
            for byte in data_list:
                new_data_str += (' ' + str(byte).strip())
            print('DATA_LENGTH: %s\t\tDATA: %s\n' % (dlc, new_data_str.strip()))
#            print('data:{}'.format(data))
            
        else:
            print('none')
        #print(str(message.data))
#        if message.arbitration_id == 0x112:
#            for key in dir(message):
#                if not '__' in key:
#                    print(key + '\t' + str(getattr(message, key)))

#    print(dir(message.data.decode('utf-8')))
#    print(message.timestamp)