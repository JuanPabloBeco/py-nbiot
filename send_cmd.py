import serial
import serial.tools.list_ports

from time import sleep

def read_extra_lines(
    ser, 
    number_of_expected_lines=4, 
    cmd='undefined', 
    print_response=True, 
    print_final_response=True, 
    ms_of_delay_after=0, 
    ms_of_delay_before=0
    ):
    
    def get_response(response, status):
        if ms_of_delay_after: sleep(ms_of_delay_after/1000)
        return({"response": response, "status": status, "cmd": cmd})

    ser.reset_input_buffer()
    if ms_of_delay_before: sleep(ms_of_delay_before/1000)

    response_lines=[]
    for i in range(0,number_of_expected_lines):
        res = ser.readline()
        res = res.decode("utf-8")
        if print_response: 
            print('> ' + res)
        #res = res.rstrip()
        response_lines.append(res)

        if (res.find('OK') == 0):
            if print_final_response and not print_response: 
                print('> ' + res)
            return(get_response(response_lines, "OK"))

        if (res.find('ERROR') == 0):
            if print_final_response and not print_response: 
                print('> ' + res)
            return(get_response(response_lines, "ERROR"))

    if print_final_response: 
        print('> ' + res)
    # print(response_lines)
    return(get_response(response_lines, "UNFINISHED"))


def send_cmd(
    cmd, 
    ser, 
    number_of_expected_lines=4, 
    print_response=True, 
    print_final_response=True, 
    ms_of_delay_after=0, 
    ms_of_delay_before=0,
    custom_response_end='',
    ):
    
    def get_response(response, 
    status):
        if ms_of_delay_after: sleep(ms_of_delay_after/1000)
        return({"response": response, "status": status, "cmd": cmd})

    ser.reset_input_buffer()

    if ms_of_delay_before: sleep(ms_of_delay_before/1000)


    cmd = cmd + "\r"
    ser.write(cmd.encode())
    print(cmd)

    response_lines=[]
    for i in range(0,number_of_expected_lines):
        res = ser.readline()
        res = res.decode("utf-8")
        if print_response: 
            print('> ' + res)
        #res = res.rstrip()
        response_lines.append(res)

        if (res.find('OK') == 0):
            if print_final_response and not print_response: 
                print('> ' + res)
            return(get_response(response_lines, "OK"))

        if (res.find('ERROR') == 0):
            if print_final_response and not print_response: 
                print('> ' + res)
            return(get_response(response_lines, "ERROR"))

        if (custom_response_end != ''):
            if (res.find(custom_response_end) == 0):
                if print_final_response and not print_response: 
                    print('> ' + res)
                return(get_response(response_lines, "OK"))

    if print_final_response: 
        print('> ' + res)
    # print(response_lines)
    return(get_response(response_lines, "UNFINISHED"))
