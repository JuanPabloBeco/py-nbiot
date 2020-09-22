import serial

from send_cmd import send_cmd
from constants import MY_PHONE_PASS

def setup_PDP_context(ser, id=1, response_history=[], retries=3, custom_delay=2000, print_response=True):
    status = 'first_round'
    while True:
        if status.find('OK') != -1 or status.find('ERROR') != -1 or retries == 0:
            check_PDP_response = check_PDP_context(ser, id, retries=retries, response_history=response_history, custom_delay=custom_delay, print_response=print_response)
            return(check_PDP_response)
        else:
            activate_PDP_response = activate_PDP_context(ser, id, retries=retries, response_history=response_history, custom_delay=custom_delay, print_response=print_response)
            #response_history.append(activate_PDP_response['response_history'])
            status=activate_PDP_response['status']
            retries-=1

def activate_PDP_context(ser, id=1, response_history=[], retries=3, custom_delay=2000, print_response=True):
    cmd_response = send_cmd("AT+QIACT="+str(id), ser,  print_response=print_response)
    #TODO: check if there is and 'ERROR' response maybe because it was already turn on
    response_history.append(cmd_response)
    for response in cmd_response['response']:     
        print(response)
        if response.find('OK') != -1:
            return({"response_history": response_history, "status": 'OK', "message": cmd_response['response'][0]})
        elif response.find('ERROR') != -1:
            return({"response_history": response_history, "status": 'ERROR', "message": cmd_response['response'][0]})
        else:
            print('otro')
    return({"response_history": response_history, "status": 'OTRO', "message": cmd_response['response'][0]})

def deactivate_PDP_context(ser, id=1, response_history=[], retries=3, custom_delay=2000, print_response=True):
    cmd_response = send_cmd("AT+QIDEACT="+str(id), ser,  print_response=print_response)
    response_history.append(cmd_response)
    for response in cmd_response['response']:     
        print(response)
        if response.find('OK') != -1:
            return({"response_history": response_history, "status": 'OK', "message": cmd_response['response'][0]})
        elif response.find('ERROR') != -1:
            return({"response_history": response_history, "status": 'ERROR', "message": cmd_response['response'][0]})
        else:
            print('otro')
    return({"response_history": response_history, "status": 'OTRO', "message": cmd_response['response'][0]})

def check_PDP_context(ser, id=1, retries=3, response_history=[], custom_delay=2000, print_response=True):
    while True:
        cmd_response = send_cmd("AT+QIACT?", ser, print_response=True, ms_of_delay_after=custom_delay)
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
