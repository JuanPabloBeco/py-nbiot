import serial
import json

from send_cmd import send_cmd
from constants import MY_PHONE_PASS

def start_up_nbiot(ser):
    response_history=[]

    cmd_response = send_cmd("AT", ser,  print_response=True, ms_of_delay_after=100)
    response_history.append(cmd_response)

    enter_pin_response = enter_pin(ser, response_history)
    if enter_pin_response["status"] == "ERROR":
        return(enter_pin_response)
    
    check_nbiot_response = check_nbiot_conection(ser, response_history=enter_pin_response["response_history"])
    if check_nbiot_response["status"] == "ERROR":
        return(check_nbiot_response)
    return(check_nbiot_response)

    #TODO: log response_history
    #TODO: check if retries are needed

def check_nbiot_conection(ser, retries=3, response_history=[], custom_delay=2000):
    while True:
        cmd_response = send_cmd("AT+CEREG?", ser, 4, print_response=True, ms_of_delay_after=custom_delay)
        response_history.append(cmd_response)
        detailed_cmd_response = cmd_response["response"][1][0:-2] # [0,-2] to remove \r\n

        if detailed_cmd_response == "+CEREG: 0,1":
            message = "Registered, home network - " + detailed_cmd_response
            status = "OK"
            break
        elif detailed_cmd_response == "+CEREG: 0,0":
            retries = retries -1
            if retries == 0:
                message = "Not registered. MT is not currently searching an operator to register to - " + detailed_cmd_response
                status = "ERROR"
                break
        elif detailed_cmd_response == "+CEREG: 0,2":
            retries = retries -1
            if retries == 0:
                message = "Not registered, but MT is currently trying to attach or searching an operator to register to - " + detailed_cmd_response
                status = "ERROR"
                break
        elif detailed_cmd_response == "+CEREG: 0,3":
            message = "Registration denied - " + detailed_cmd_response
            status = "ERROR"
            break
        elif detailed_cmd_response == "+CEREG: 0,4":
            message = "Unknown - " + detailed_cmd_response
            status = "ERROR"
            break
        elif detailed_cmd_response == "+CEREG: 0,5":
            message = "Registered, roaming - " + detailed_cmd_response
            status = "OK"
            break
        else:
            retries -= 1
            if retries == 0:
                message = "Unknown error - " + detailed_cmd_response
                status = "ERROR"
                break

    print('\r\n' + status + ' - ' + message + '\r\n')
    return({"response_history": response_history, "status": status, "message": message})

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

