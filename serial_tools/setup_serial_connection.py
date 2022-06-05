import sys
sys.path.append( '..' )

import serial
import serial.tools.list_ports

import utils.configuration as configuration
import custom_test_connection
import custom_test_mqtt
import utils.PDP_context as PDP_context
import utils.ping as ping
import utils.MQTT as MQTT

from serial_tools.send_cmd import send_cmd, read_extra_lines

def setup_serial_connection():
    list = serial.tools.list_ports.comports()
    print(*list)

    return serial.Serial(port='COM4', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=5)
