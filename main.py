from constants import MY_PHONE_PASS
from configuration import start_up_nbiot
from PDP_context import setup_PDP_context
from ping import  ping

import serial
import serial.tools.list_ports
from print_cmd_history import print_cmd_history
from send_cmd import send_cmd

list = serial.tools.list_ports.comports()
print(*list)

ser = serial.Serial(port='COM4', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=5)

response = start_up_nbiot(ser)

response = setup_PDP_context(ser, response_history=response["response_history"])

print_cmd_history(response)

#print(ping(ser, response_history=response["response_history"]))

ser.close()



