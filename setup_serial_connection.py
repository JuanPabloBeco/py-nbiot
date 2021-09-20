import serial
import serial.tools.list_ports

import configuration
import custom_test_connection
import custom_test_mqtt
import PDP_context
import ping
import MQTT

from send_cmd import send_cmd, read_extra_lines

ser = serial.Serial(port='COM3', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=5)

# def setup_serial_connection():
#     list = serial.tools.list_ports.comports()
#     print(*list)

#     return serial.Serial(port='COM4', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=5)
