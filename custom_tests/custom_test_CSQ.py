import sys

sys.path.append( '..' )

from utils.get_network_location_report import get_network_location_report
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
from utils.acquire_signal_quality_report import acquire_signal_quality_report
from utils.acquire_GNSS_position import turn_on_GNSS, acquire_GNSS_position, turn_off_GNSS

import csv

'''

Test to log signal strength 

Run on just turned on nb-iot modem 

'''

DEFAULT_COM_PORT = 'COM3'

def custom_test_CSQ(ser=-1):
    list = serial.tools.list_ports.comports()
    print(*list)
    if (ser == -1):
        ser = serial.Serial(port=DEFAULT_COM_PORT, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=5)
    
    f = open("test.txt", "a")

    startTime = datetime.now()
    
    f.write("\n\n\n")
    f.write("Start CSQ test at - ")
    f.write(str(startTime))
    f.write("\n")

    
    response = optimized_start_up_nbiot(ser)

    connectingTime = datetime.now()

    f.write("\n")
    f.write("End connecting at - ")
    f.write(str(connectingTime))
    f.write("\n")

    f.write("Start sending CSQ")
    f.write("\n")
    f.write("\n")

    f.write("CSQ:\nrssi, ber, status, date")
    f.write("\n")

    while True:
        f = open("test.txt", "a")

        cmd_response = send_cmd("AT+CSQ", ser, print_final_response=False)
        readingTime = datetime.now()

        f.write(str(cmd_response['response'][1][-7:-5]))
        f.write(",")
        f.write(str(cmd_response['response'][1][-4:-2]))
        f.write(",")
        f.write(str(cmd_response['status']))
        f.write(",")
        f.write(str(readingTime))
        f.write("\n")
        f.close()

        # m_of_delay = 
        # s_of_delay = m_of_delay/60

        s_of_delay = 1

        sleep(s_of_delay)
    # print_cmd_history(response)

    ser.close()

    return response

def custom_test_acquire_signal_quality_and_GNSS_position(ser=-1, s_of_delay=1):
    list = serial.tools.list_ports.comports()
    print(*list)
    if (ser == -1):
        ser = serial.Serial(port=DEFAULT_COM_PORT, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=5)
    
    startTime = datetime.now()
    log_file_name = "nbiot_test_mvd_v2_" + startTime.strftime('%Y_%m_%d_%H_%M_%S') + ".csv" # ".txt"
    f = open(log_file_name, "w")

    
    response = optimized_start_up_nbiot(ser)
    print(response)
    
    response = turn_on_GNSS(ser, 1, 3, 0, 1)
    print(response)

    connectingTime = datetime.now()

    f.write("rssi,ber,status,date,utc,lat,lng,hdop,altitude,fix,cog,spkm,spkn,nsat")
    f.write("\n")
    f.close()
    
    while True:
        f = open(log_file_name, "a")
        
        GNSS_position = acquire_GNSS_position(ser)
        response = turn_off_GNSS(ser)
        print(response)

        signal_quality_report = acquire_signal_quality_report(ser)


        response = turn_on_GNSS(ser, 1, 1, 0, 1) # dejar encendido el GPS para poder aprobechar el tiempo de sleep en fijar la posicion
        print(response)

        print("step summary:")

        if signal_quality_report['status']=='OK':
            f.write(str(signal_quality_report['rssi']))
            print('rssi = ' + str(signal_quality_report['rssi']))
            f.write(",")
            f.write(str(signal_quality_report['ber']))
            f.write(",")
            f.write(str(signal_quality_report['status']))
            f.write(",")
            f.write(str(signal_quality_report['date']))
            f.write(",")
        else:
            f.write('-1')
            print('rssi = -1')
            f.write(",")
            f.write('-1')
            f.write(",")
            f.write('-1')
            f.write(",")
            f.write('-1')
            f.write(",")
        
        if GNSS_position['status']=='OK':
            f.write(str(GNSS_position['utc']))
            f.write(",")
            f.write(str(GNSS_position['lat']))
            print('lat = ' + str(GNSS_position['lat']))
            f.write(",")
            f.write(str(GNSS_position['lng']))
            print('lng = ' + str(GNSS_position['lng']))
            f.write(",")
            f.write(str(GNSS_position['hdop']))
            f.write(",")
            f.write(str(GNSS_position['altitude']))
            f.write(",")
            f.write(str(GNSS_position['fix']))
            f.write(",")
            f.write(str(GNSS_position['cog']))
            f.write(",")
            f.write(str(GNSS_position['spkm']))
            f.write(",")
            f.write(str(GNSS_position['spkn']))
            # f.write(",")
            # f.write(str(GNSS_position['date']))
            f.write(",")
            f.write(str(GNSS_position['nsat']))
            f.write("\n")
        else:
            f.write('-1')
            f.write(",")
            f.write('-1')
            print('lat = -1')
            f.write(",")
            f.write('-1')
            print('lng = -1')
            f.write(",")
            f.write('-1')
            f.write(",")
            f.write('-1')
            f.write(",")
            f.write('-1')
            f.write(",")
            f.write('-1')
            f.write(",")
            f.write('-1')
            f.write(",")
            f.write('-1')
            # f.write(",")
            # f.write('-1')
            f.write(",")
            f.write('-1')
            f.write("\n")
        f.close()

        print("/n/n")

        sleep(s_of_delay)
    # print_cmd_history(response)

    ser.close()

    return response

def custom_test_acquire_signal_quality_with_network_information(ser=-1, s_of_delay=1, activate_gnss=False):
    startTime = datetime.now()

    log_file_name = "nbiot_test_mvd_v2_" + startTime.strftime('%Y_%m_%d_%H_%M_%S') + ".csv" # ".txt"

    f = open(log_file_name, "w")

    list = serial.tools.list_ports.comports()
    print(*list)
    if (ser == -1):
        ser = serial.Serial(port=DEFAULT_COM_PORT, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=5)
    
    
    response = optimized_start_up_nbiot(ser)
    print(response)
    
    if activate_gnss:
        response = turn_on_GNSS(ser, 1, 3, 0, 1)
        print(response)

    connectingTime = datetime.now()

    file_header = "rssi,ber,status,date,"
    file_header += 'n,stat,tracking_area_code,cell_id,access_technology,network_query_status,network_query_date'
    if activate_gnss:
        file_header += 'utc,lat,lng,hdop,altitude,fix,cog,spkm,spkn,nsat'

    f.write(file_header)
    f.write("\n")
    f.close()
    
    while True:
        f = open(log_file_name, "a")
        
        if activate_gnss:
            GNSS_position = acquire_GNSS_position(ser)
            response = turn_off_GNSS(ser)
            print(response)

        signal_quality_report = acquire_signal_quality_report(ser)
        network_location_report = get_network_location_report(ser)

        if activate_gnss:
            response = turn_on_GNSS(ser, 1, 1, 0, 1) # dejar encendido el GPS para poder aprobechar el tiempo de sleep en fijar la posicion
            print(response)

        print("step summary:")

        if signal_quality_report['status']=='OK':
            print('rssi = ' + str(signal_quality_report['rssi']))
            f.write(str(signal_quality_report['rssi']) + ",")
            f.write(str(signal_quality_report['ber']) + ",")
            f.write(str(signal_quality_report['status']) + ",")
            f.write(str(signal_quality_report['date']) + ",")
        else:
            print('rssi = -1')
            f.write('-1,')
            f.write('-1,')
            f.write('-1,')
            f.write('-1')

        if network_location_report['status']=='OK':
            print('stat = ' + str(network_location_report['stat']))
            print('cell_id = ' + str(network_location_report['cell_id']))
            print('access_technology = ' + str(network_location_report['access_technology']))
            f.write(str(network_location_report['n']) + ",")
            f.write(str(network_location_report['stat']) + ",")
            f.write(str(network_location_report['tracking_area_code']) + ",")
            f.write(str(network_location_report['cell_id']) + ",")
            f.write(str(network_location_report['access_technology']) + ",")
            f.write(str(network_location_report['status']) + ",")
            f.write(str(network_location_report['date']) + ",")
        else:
            print('rssi = -1')
            f.write('-1,')
            f.write('-1,')
            f.write('-1,')
            f.write('-1,')
            f.write('-1,')
            f.write('-1,')
            f.write('-1')
        
        if activate_gnss:
            if GNSS_position['status']=='OK':
                print('lat = ' + str(GNSS_position['lat']) + ",")
                print('lng = ' + str(GNSS_position['lng']) + ",")
                f.write(str(GNSS_position['utc']) + ",")
                f.write(str(GNSS_position['lat']) + ",")
                f.write(str(GNSS_position['lng']) + ",")
                f.write(str(GNSS_position['hdop']) + ",")
                f.write(str(GNSS_position['altitude']) + ",")
                f.write(str(GNSS_position['fix']) + ",")
                f.write(str(GNSS_position['cog']) + ",")
                f.write(str(GNSS_position['spkm']) + ",")
                f.write(str(GNSS_position['spkn']) + ",")
                # f.write(str(GNSS_position['date']) + ",")
                f.write(str(GNSS_position['nsat']) + ",")
            else:
                print('lat = -1')
                print('lng = -1')
                f.write('-1,')
                f.write('-1,')
                f.write('-1,')
                f.write('-1,')
                f.write('-1,')
                f.write('-1,')
                f.write('-1,')
                f.write('-1,')
                f.write('-1,')
                # f.write('-1,')
                f.write('-1')

        f.write("\n")
        f.close()

        print("/n/n")

        sleep(s_of_delay)
    # print_cmd_history(response)

    ser.close()

    return response