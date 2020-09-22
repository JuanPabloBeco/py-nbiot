import serial

from send_cmd import send_cmd, read_extra_lines
from constants import MY_PHONE_PASS

def ping(ser, context_id=1, host="8.8.8.8", timeout= 0, pingnum= 0, response_history=[], retries=3, custom_delay=2000, print_response=True):
    cmd = "AT+QPING=" + str(context_id) + "," + "\"" + host + "\""
    number_of_expected_lines=2*(4+1)

    if timeout!=0:
        cmd+=","+str(timeout)
    if pingnum!=0: 
        cmd+=","+str(pingnum)
        number_of_expected_lines=2*(pingnum+1)
    cmd_response = send_cmd(cmd, ser,  print_response=print_response, ms_of_delay_after=200)
    
    message = "No response"
    for response in cmd_response['response']:
        if response.find('OK') != -1:
            cmd_response_extra_lines = read_extra_lines(ser, number_of_expected_lines=number_of_expected_lines, cmd=cmd)
            
            cmd_response['response'].extend(cmd_response_extra_lines['response'])
            break
    
    response_history.append(cmd_response['response'])

    if len(cmd_response_extra_lines['response'][-1])==0:
        message = "Problems in ping response"
    else:
        message = cmd_response_extra_lines['response'][-1]
    
    return({"response_history": response_history, "status": cmd_response['status'], "message": message})
