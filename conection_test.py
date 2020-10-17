from constants import MY_PHONE_PASS
from configuration import optimized_start_up_nbiot
from PDP_context import optimized_setup_PDP_context
from ping import  ping

import serial
import serial.tools.list_ports
from print_cmd_history import print_cmd_history
from send_cmd import send_cmd

'''
The objective of this test is to measure the energy needed to conect the modem to nb-iot
to do so it starts the serial port, sends the SIM PIN, conect to the network already configured
and setup the PDP context and sends executes a ping to check communications 

Observation: To really measure energy further hardware is needed

'''

def conection_test():
list = serial.tools.list_ports.comports()
print(*list)

ser = serial.Serial(port='COM4', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=5)

response = optimized_start_up_nbiot(ser)

response = optimized_setup_PDP_context(ser, response_history=response["response_history"], retries=3, custom_delay=1000)

print(ping(ser, response_history=response["response_history"]))

print_cmd_history(response)

ser.close()



