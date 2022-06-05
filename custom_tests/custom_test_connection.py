import sys

sys.path.append( '..' )

from constants import MY_PHONE_PASS
from utils.configuration import optimized_start_up_nbiot
from utils.PDP_context import optimized_setup_PDP_context
from utils.ping import  ping

import serial
import serial.tools.list_ports
from serial_tools.print_cmd_history import print_cmd_history
from serial_tools.send_cmd import send_cmd

'''
The objective of this test is to measure the energy needed to conect the modem to nb-iot
to do so it starts the serial port, sends the SIM PIN, conect to the network already configured
and setup the PDP context and sends executes a ping to check communications 

Observation: To really measure energy further hardware is needed

'''

def custom_test_connection(ser=-1):
    list = serial.tools.list_ports.comports()
    print(*list)
    if (ser == -1):
        ser = serial.Serial(port='COM3', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=5)

    response = optimized_start_up_nbiot(ser)

    response = optimized_setup_PDP_context(ser, response_history=response["response_history"], retries=3, custom_delay=1000)

    response = ping(ser, response_history=response["response_history"])

    print(response)

    ser.close()

    return response

custom_test_connection()