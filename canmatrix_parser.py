import json

path = r'/home/pi/Desktop/FAW_C105_ADAS_Network_CANDBC_V1.2forbosch_forV1.6_dDASY.dbc'
with open (path, 'rb') as file:
    bin_obj = file.read()
    dic_obj = json.loads(bin_obj.decode('ISO-8859-1'))

    
    