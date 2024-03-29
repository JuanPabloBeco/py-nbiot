import sys
sys.path.append( '..' )

import serial
import json

from serial_tools.send_cmd import send_cmd
from constants import MY_PHONE_PASS


def enter_pin(ser, response_history=[]):
    cmd_response = send_cmd("AT+CPIN?", ser, 6,  print_response=True)
    response_history.append(cmd_response)

    response_code = response_history[-1]["response"][1][0:-2] # [0:-2] to remove \r\n
    
    if response_code == "+CPIN: SIM PIN":
        cmd_response = send_cmd("AT+CPIN=" + MY_PHONE_PASS, ser, 8,  print_response=True, ms_of_delay_after=1000)
        response_history.append(cmd_response)
        response_status = response_history[-1]["status"]

        if response_status == "ERROR":
            status = "ERROR"
            message = "SIM PIN SENT AND ERROR"
        elif response_status == "OK":
            status = "OK"
            message = "SIM PIN SENT AND SUCCESS"
        else:
            status = "ERROR"
            message = "SIM PIN SENT AND UNFINISHED"
    elif response_code == "+CPIN: READY":
        status = "OK"
        message = "+CPIN: READY"
    else:
        print('==> SIM error with message ' + response_code)
        status = "ERROR"
        message = response_code
        
    return({"response_history": response_history, "status": status, "message": message})

def start_up_nbiot(ser, response_history=[]):

    cmd_response = send_cmd("AT", ser,  print_response=True, ms_of_delay_after=100)
    response_history.append(cmd_response)

    res = enter_pin(ser, response_history)
    if res["status"] == "ERROR":
        return(res)
    
    res = check_nbiot_conection(ser, response_history=res["response_history"])
    if res["status"] == "ERROR":
        return(res)
    return(res)

    #TODO: log response_history
    #TODO: check if retries are needed

def optimized_start_up_nbiot(ser, response_history=[]):

    res = enter_pin(ser, response_history)
    if res["status"] == "ERROR":
        return(res)
    
    res = check_nbiot_conection(ser, response_history=res["response_history"])
    if res["status"] == "ERROR":
        return(res)
    return(res)

    #TODO: log response_history
    #TODO: check if retries are needed

def check_nbiot_conection(ser, retries=3, response_history=[], custom_delay=2000):
    while True:
        res = send_cmd("AT+CEREG=2", ser, 4, print_response=True, ms_of_delay_after=custom_delay+2000)
        res = send_cmd("AT+CEREG?", ser, 4, print_response=True, ms_of_delay_after=custom_delay)
        response_history.append(res)
        # detailed_res = res["response"][1][0:-2] # [0,-2] to remove \r\n

        temp = res['response'][1].split('\r\n')[0]
        temp = temp.split(':')[1]
        
        temp = temp.split(',')
        [n ,stat ,tracking_area_code, cell_id, access_technology] = temp

        if stat == "1":
            message = "Registered, home network - " + stat
            status = "OK"
            break
        elif stat == "0":
            retries = retries -1
            if retries == 0:
                message = "Not registered. MT is not currently searching an operator to register to - "# + detailed_res
                status = "ERROR"
                break
        elif stat == "2":
            retries = retries -1
            if retries == 0:
                message = "Not registered, but MT is currently trying to attach or searching an operator to register to - "# + detailed_res
                status = "ERROR"
                break
        elif stat == "3":
            message = "Registration denied - " + stat
            status = "ERROR"
            break
        elif stat == "4":
            message = "Unknown - " + stat
            status = "ERROR"
            break
        elif stat == "5":
            message = "Registered, roaming - " + stat
            status = "OK"
            break
        else:
            retries -= 1
            if retries == 0:
                message = "Unknown error - " + stat
                status = "ERROR"
                break

    print('\r\n' + status + ' - ' + message + '\r\n')
    return({"response_history": response_history, "status": status, "message": message})

def turn_off(ser, response_history=[]):
    cmd_response = send_cmd("AT+QPOWD", ser,  print_response=True, ms_of_delay_after=1000)
    response_history.append(cmd_response)        
    return({"response_history": response_history, "status": "OK", "message": "Turned off"})