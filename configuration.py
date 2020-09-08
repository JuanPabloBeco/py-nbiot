import serial
import json

from send_cmd import send_cmd
from constants import MY_PHONE_PASS


def turn_on_nbiot(ser):
    response_history=[]

    cmd_response = send_cmd("AT", ser,  print_response=True, ms_of_after_delay=100)
    response_history.append(cmd_response)

    cmd_response = send_cmd("AT+CPIN?", ser, 6,  print_response=True)
    response_history.append(cmd_response)

    enter_pin_response = enter_pin(ser, response_history)
    if enter_pin_response["status"] == "ERROR":
        print(enter_pin_response["message"])
        return(enter_pin_response)
    else:
        response_history = enter_pin_response["response_history"]
    
    check_nbiot_response = check_nbiot_conection(ser, response_history=response_history)
    if check_nbiot_response["status"] == "ERROR":
        return(check_nbiot_response)
    else:
        response_history = check_nbiot_response["response_history"]
    
    activate_PDP_response = activate_PDP_context(ser, response_history=response_history)
    if enter_pin_response["status"] == "ERROR":
        return(activate_PDP_response)
    else:
        response_history = activate_PDP_response["response_history"]
    deactivate_PDP_context(ser, response_history=response_history)
    print(response_history)

    #TODO: log response_history

def check_nbiot_conection(ser, retries=3, response_history=[], custom_delay=2000):
    while True:
        cmd_response = send_cmd("AT+CEREG?", ser, 4, print_response=True, ms_of_after_delay=custom_delay)
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
            retries = retries -1
            if retries == 0:
                message = "Unknown error - " + detailed_cmd_response
                status = "ERROR"
                break

    print('\r\n' + status + ' - ' + message + '\r\n')
    return({"response_history": response_history, "status": status, "message": message})

def deactivate_PDP_context(ser, id=1, response_history=[], retries=3, custom_delay=2000, print_response=True):
    cmd_response = send_cmd("AT+QIDEACT="+str(id), ser, 4,  print_response=print_response)
    return(cmd_response)

def activate_PDP_context(ser, id=1, response_history=[], retries=3, custom_delay=2000, print_response=True):
    cmd_response = send_cmd("AT+QIACT="+str(id), ser, 4,  print_response=print_response)
    #TODO: check if there is and 'ERROR' response maybe because it was already turn on
    response_history.append(cmd_response)

    check_PDP_response = check_PDP_context(ser, id, retries=retries, response_history=response_history, custom_delay=custom_delay, print_response=print_response)
    return(check_PDP_response)
    #TODO: if required add retries to the activation of the pdp context


def check_PDP_context(ser, id=1, retries=3, response_history=[], custom_delay=2000, print_response=True):
    while True:
        cmd_response = send_cmd("AT+QIACT?", ser, 4, print_response=True, ms_of_after_delay=custom_delay)
        response_history.append(cmd_response)
        detailed_cmd_response = cmd_response["response"][1][0:-2] # [0,-2] to remove \r\n
        
        if detailed_cmd_response.find(': ' + str(id) + ',1') != -1:
            message = "PDP context ' + str(id) + ' Activated - " + detailed_cmd_response
            status = "OK"
            break

        elif detailed_cmd_response.find(': ' + str(id) + ',0') != -1:
            retries = retries -1
            if retries == 0:
                message = "PDP context ' + str(id) + ' Deactivated - " + detailed_cmd_response
                status = "ERROR"
                break
        elif detailed_cmd_response == 'OK':
            message = "PDP context not activated yet - " + detailed_cmd_response
            status = "ERROR"
            break
        else:
            retries = retries -1
            if retries == 0:
                message = "Unknown error - " + detailed_cmd_response
                status = "ERROR"
                break
    if print_response:
        print('\r\n' + status + ' - ' + message + '\r\n')
    return({"response_history": response_history, "status": status, "message": message})


def enter_pin(ser, response_history=[]):
    cmd_response = send_cmd("AT+CPIN?", ser, 6,  print_response=True)
    response_history.append(cmd_response)

    response_code = response_history[-1]["response"][1][0:-2] # [0:-2] to remove \r\n
    
    if response_code == "+CPIN: SIM PIN":
        cmd_response = send_cmd("AT+CPIN=" + MY_PHONE_PASS, ser, 8,  print_response=True, ms_of_after_delay=1000)
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

