from constants import MY_PHONE_PASS
from configuration import optimized_start_up_nbiot
from PDP_context import optimized_setup_PDP_context
from MQTT import publish_mqtt_message, open_mqtt_network, connect_to_mqtt_server, check_connection_to_mqtt_server

import serial
import serial.tools.list_ports
from print_cmd_history import print_cmd_history
from send_cmd import send_cmd

from datetime import datetime
from time import sleep
from acquire_signal_quality_report import acquire_signal_quality_report
from acquire_GNSS_position import turn_on_GNSS, acquire_GNSS_position, turn_off_GNSS

import csv

'''

Test to log signal strength 

Run on just turned on nb-iot modem 

'''

def custom_test_CSQ(ser=-1):
    list = serial.tools.list_ports.comports()
    print(*list)
    if (ser == -1):
        ser = serial.Serial(port='COM3', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=5)
    
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

        cmd_response = send_cmd("AT+CSQ", ser, 
    print_final_response=False, )
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
        ser = serial.Serial(port='COM3', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=5)
    
    startTime = datetime.now()

    log_file_name = "nbiot_test_mvd_v2_" + startTime.strftime('%Y_%m_%d_%H_%M_%S') + ".csv" # ".txt"

    # f = open("test_" + str(startTime) +".txt", "w")
    f = open(log_file_name, "w")
    
    # f.write("\n\n\n")
    # f.write("Start CSQ test at - ")
    # f.write(str(startTime))
    # f.write("\n")

    
    response = optimized_start_up_nbiot(ser)
    print(response)
    
    response = turn_on_GNSS(ser, 1, 3, 0, 1)
    print(response)

    connectingTime = datetime.now()

    # f.write("\n")
    # f.write("End connecting at - ")
    # f.write(str(connectingTime))
    # f.write("\n")

    # f.write("Start sending CSQ")
    # f.write("\n")
    # f.write("\n")

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
        
        # csv.DictWriter(csvfile)
        # writer.writerow(data)

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

        # m_of_delay = 
        # s_of_delay = m_of_delay/60
        # s_of_delay = 1


        sleep(s_of_delay)
    # print_cmd_history(response)

    ser.close()

    return response

custom_test_acquire_signal_quality_and_GNSS_position()
