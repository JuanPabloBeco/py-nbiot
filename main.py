from constants import MY_PHONE_PASS
from configuration import turn_on_nbiot

import serial
import serial.tools.list_ports

from send_cmd import send_cmd

list = serial.tools.list_ports.comports()
print(*list)

ser = serial.Serial(port='COM4', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=5)

response = turn_on_nbiot(ser)

ser.close()

