import sys
sys.path.append( '..' )

import serial

from serial_tools.send_cmd import send_cmd
from constants import MY_PHONE_PASS

DEFALUT_PRINT_RESPONSE = True
DEFAULT_TCP_CONNECT_ID = 0
DEFAULT_HOST_NAME = "54.191.221.113"
DEFAULT_PORT = 1883
DEFAULT_USERNAME = "topic"
DEFEULT_PASSWORD = "password o string secreto"

DEFAULT_TCP_CONNECT_ID = 0
DEFAULT_MSG_ID = 0
DEFAULT_QOS = 0
DEFAULT_RETAIN = 0
DEFAULT_TOPIC = "mychannel"


def check_mqtt_network(ser,  print_response=DEFALUT_PRINT_RESPONSE):
    cmd_response = send_cmd("AT+QMTOPEN?", ser,  print_response=print_response)
    print(cmd_response)
    return(cmd_response)

def open_mqtt_network(
    ser, 
    tcp_connect_id=DEFAULT_TCP_CONNECT_ID, 
    host_name=DEFAULT_HOST_NAME, 
    port=DEFAULT_PORT, 
    print_response=DEFALUT_PRINT_RESPONSE,
    ):
    cmd_response = send_cmd("AT+QMTOPEN=" + str(tcp_connect_id) + ",\"" + host_name + "\"" + "," + str(port), ser,  print_response=print_response)
    print(cmd_response)
    return(cmd_response)

def connect_to_mqtt_server(
    ser, 
    tcp_connect_id=DEFAULT_TCP_CONNECT_ID, 
    username = DEFAULT_USERNAME, 
    password = DEFEULT_PASSWORD,
    print_response=DEFALUT_PRINT_RESPONSE,
    ):
    cmd_response = send_cmd(
        "AT+QMTCONN=" + str(tcp_connect_id) + ",\"" + username + "\",\"" + password + "\"", 
        ser,  
        print_response=print_response, 
        ms_of_delay_before=100)

    print(cmd_response)
    return(cmd_response)

def check_connection_to_mqtt_server(
    ser,
    print_response=DEFALUT_PRINT_RESPONSE,
    tcp_connect_id=DEFAULT_TCP_CONNECT_ID, 
    base_delay=500,
    ):
    cmd_response={'status':'ERROR'}
    print('check_connection_to_mqtt_server')
    
    for time in range(0,3):
        cmd_response = send_cmd(
            "AT+QMTCONN?", 
            ser,  
            ms_of_delay_before=base_delay*(time+1),
            print_response=print_response)
        print('cmd_response: ')
        print(cmd_response)
        print(cmd_response.get('response')[1])

        if cmd_response.get('response')[1].find('OK') != -1:
            print(cmd_response.get('response')[1].find('OK'))
            return(cmd_response)
        if cmd_response.get('response')[1].split(str(tcp_connect_id) + ",",1)[1][0] == '3':
            print(cmd_response.get('response')[1].split(str(tcp_connect_id) + ",",1)[1][0])
            return(cmd_response)
    
    cmd_response['status'] = 'TIMEOUT'
    print('TIMEOUT')
    return(cmd_response)

def publish_mqtt_message(
    ser, 
    str_to_send,
    topic = DEFAULT_TOPIC,
    tcp_connect_id = DEFAULT_TCP_CONNECT_ID,
    msgID = DEFAULT_MSG_ID,
    qos = DEFAULT_QOS,
    retain = DEFAULT_RETAIN,
    print_response=DEFALUT_PRINT_RESPONSE
    ):
    cmd_response = send_cmd(
        "AT+QMTPUB=" + 
        str(tcp_connect_id) + "," + 
        str(msgID) + "," + 
        str(qos) + "," + 
        str(retain) + "," + 
        "\"" + topic + "\"," + 
        str(len(str_to_send)), # these length is in bytes 
        ser,  
        custom_response_end='>',
        print_response=print_response
    )
    print(cmd_response)

    cmd_response = send_cmd(str_to_send, ser,  print_response=print_response, ms_of_delay_before=200)
    print(cmd_response)
    return cmd_response

def close_mqtt_network(ser, tcp_connect_id=DEFAULT_TCP_CONNECT_ID, print_response=DEFALUT_PRINT_RESPONSE):
    cmd_response = send_cmd("AT+QMTCLOSE=" + str(tcp_connect_id) + "", ser,  print_response=print_response)
    print(cmd_response)

def disconnect_to_mqtt_server(ser,  print_response=DEFALUT_PRINT_RESPONSE):
    cmd_response = send_cmd("AT+QMTDISC=" + str(tcp_connect_id) + "", ser,  print_response=print_response)
    print(cmd_response)
    return(cmd_response)

def subscribe_to_mqtt_topic(ser,  print_response=DEFALUT_PRINT_RESPONSE):
    cmd_response = send_cmd("AT+QMTSUB=0,1,\"mychannel\",0", ser,  print_response=print_response)
    print(cmd_response)
    return(cmd_response)

def subscribe_to_mqtt_topic(ser,  print_response=DEFALUT_PRINT_RESPONSE):
    cmd_response = send_cmd("AT+QMTUNS=0,1,\"mychannel\"", ser,  print_response=print_response)
    print(cmd_response)
    return(cmd_response)
