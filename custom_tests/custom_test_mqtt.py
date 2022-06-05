import sys

sys.path.append( '..' )

from constants import MY_PHONE_PASS
from utils.configuration import optimized_start_up_nbiot
from utils.PDP_context import optimized_setup_PDP_context
from utils.MQTT import publish_mqtt_message, open_mqtt_network, connect_to_mqtt_server, check_connection_to_mqtt_server

import serial
import serial.tools.list_ports
from serial_tools.print_cmd_history import print_cmd_history
from serial_tools.send_cmd import send_cmd

from datetime import datetime

from time import sleep

'''
The objective of this test is to measure the energy needed to publish messages of different lengths
using mqtt protocol

Observation: To measure energy further hardware is needed

'''

def custom_test_mqtt(ser=-1, msg_length=10, nbiot_connected = False):
    list = serial.tools.list_ports.comports()
    print(*list)
    if (ser == -1):
        ser = serial.Serial(port='COM3', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=5)
    if not nbiot_connected:
        response = optimized_start_up_nbiot(ser)

        response = optimized_setup_PDP_context(ser, response_history=response["response_history"], retries=3, custom_delay=1000)

    mqtt_check = check_connection_to_mqtt_server(ser)

    mqtt_open = {}
    mqtt_connect = {}

    for time in range(0,3):

        print(mqtt_open)
        if mqtt_open.get('status') != 'OK': mqtt_open = open_mqtt_network(ser)
        print(mqtt_open)
        if mqtt_open.get('status') != 'OK': break
        
        mqtt_check = check_connection_to_mqtt_server(ser)

        print(mqtt_connect)
        if mqtt_connect.get('status') != 'OK': mqtt_connect = connect_to_mqtt_server(ser)
        print(mqtt_connect)
        if mqtt_connect.get('status') != 'OK': break

        mqtt_check = check_connection_to_mqtt_server(ser)

    if mqtt_check.get('status') == 'OK':
        start = datetime.now()
        response = publish_mqtt_message(ser, 'a'*msg_length)
        end = datetime.now()
        diff = end-start
        print('tiempo: ' + str(diff))
        cmd_response = send_cmd("AT+CSQ", ser)

    ser.close()
    return response

def custom_test_mqtt_iterative(
    ser=-1, 
    msg_length_start=10, 
    msg_length_end=100, 
    msg_length_step_size=10, 
    nbiot_connected = False,
    is_connected_to_mqtt_broker = True,
    wait=True,
    ):
    list = serial.tools.list_ports.comports()
    print(*list)
    if (ser == -1):
        ser = serial.Serial(port='COM3', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=5)
    
    if not nbiot_connected:
        response = optimized_start_up_nbiot(ser)
        response = optimized_setup_PDP_context(ser, response_history=response["response_history"], retries=3, custom_delay=1000)
    
    if not is_connected_to_mqtt_broker:
        open_mqtt_network(ser)
        sleep(1)
        connect_to_mqtt_server(ser)
        sleep(1)

    for msg_length in range(msg_length_start, msg_length_end+1, msg_length_step_size):
        start = datetime.now()
        response = publish_mqtt_message(ser, 'a'*msg_length)
        end = datetime.now()
        diff = end-start
        print('tiempo: ' + str(diff) + '\n')
        # if wait & msg_length < msg_length_end: # corregir para que no se llame la ultima vez
            # input(str(msg_length) + " - press Enter to continue...")

        cmd_response = send_cmd("AT+CSQ", ser, ms_of_delay_before=5000 )

    ser.close()
    return response

custom_test_mqtt_iterative(msg_length_start=10, msg_length_end=1010, msg_length_step_size=250, nbiot_connected = True, wait=False)
