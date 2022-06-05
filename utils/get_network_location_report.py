import sys
sys.path.append( '..' )

import serial
from serial_tools.send_cmd import send_cmd
from datetime import datetime
import json

def get_network_location_report(ser):
    '''
        This requires the previous configuration of AT+CEREG=2
    '''
    print('get_network_location_report')
    cmd_response = send_cmd("AT+CEREG?", ser, print_final_response=False )
    
    # print(json.dumps(cmd_response, sort_keys=True, indent=4))

    temp = cmd_response['response'][1].split('\r\n')[0]
    temp = temp.split(':')[1]
    temp = temp.split(',')

    [n ,stat ,tracking_area_code, cell_id, access_technology] = temp
    status=cmd_response['status']
    
    readingTime = datetime.now()
    date=readingTime

    outDictionary = {
        'n': n,
        'stat': stat,
        'tracking_area_code': tracking_area_code,
        'cell_id': cell_id,
        'access_technology': access_technology,
        'status': status,
        'date': date,
    }

    print(outDictionary)
    print('\n\n')

    return outDictionary

# ser = serial.Serial(port='COM3', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=5)
# get_network_location_report(ser)
# ser.close()
