import serial
import serial.tools.list_ports

from time import sleep

def send_cmd(cmd, ser, number_of_expected_lines=4, print_response=True, print_final_response=True, ms_of_after_delay=0):
    
    def get_response(response, status):
        if ms_of_after_delay: sleep(ms_of_after_delay/1000)
        return({"response": response, "status": status, "cmd": cmd})

    ser.reset_input_buffer()

    cmd = cmd + "\r"
    ser.write(cmd.encode())
    print(cmd)

    response_lines=[]
    for i in range(0,number_of_expected_lines):
        res = ser.readline()
        res = res.decode("utf-8")
        if print_response: 
            print('> ' + res)
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
