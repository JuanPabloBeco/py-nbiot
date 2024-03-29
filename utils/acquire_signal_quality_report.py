import sys
sys.path.append( '..' )

import serial
from serial_tools.send_cmd import send_cmd
from datetime import datetime
import json

def acquire_signal_quality_report(ser):
    print('acquire_signal_quality_report')
    cmd_response = send_cmd("AT+CSQ", ser, print_final_response=False )
    
    print(json.dumps(cmd_response, sort_keys=True, indent=4))

    rssi=cmd_response['response'][1][-7:-5]
    ber=cmd_response['response'][1][-4:-2]
    status=cmd_response['status']
    
    readingTime = datetime.now()
    date=readingTime

    outDictionary = {
        'rssi': rssi,
        'ber': ber,
        'status': status,
        'date': date,
    }

    print(outDictionary)
    print('\n\n')

    return outDictionary
