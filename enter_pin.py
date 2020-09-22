from constants import MY_PHONE_PASS

import serial

from send_cmd import send_cmd

import json
def enter_pin(ser):
    response_history=[]

    #cmd_response = send_cmd("AT", ser,  print_response=True, ms_of_delay_after=100)
    #response_history.append(cmd_response)
    cmd_response = send_cmd("AT+CPIN?", ser, 6,  print_response=True)
    response_history.append(cmd_response)
    cmd_response = send_cmd("AT+CPIN=" + MY_PHONE_PASS, ser, 8,  print_response=True, ms_of_delay_after=10000)
    response_history.append(cmd_response)

    if response_history[-1]["status"] == "ERROR":
        response = {"status": "CPIN ERROR", "response_history": response_history}
        #print("\n---->" + json.dumps(response))
        return(response)

    #do while response != 0,1 y ver si hacerlo saltar despues de que pase 2 o 3 veces
    
    cmd_response = send_cmd("AT+CEREG?", ser, 4, print_response=True, ms_of_delay_after=15000)
    response_history.append(cmd_response)

    detailed_response = [s for s in response_history[-1] if "+" in s]
    print(json.dumps(detailed_response))
    if detailed_response.find("0,0"):
        #incompleto esperar y probar de nuevo
        print("0,0")
    elif detailed_response.find("0,1"):
        #listo adelante
        print("0,1")
    else:
        #error ni idea que esta pasando :(
        response = {"status": "NB-IOT CONECTION ERROR", "message": detailed_response,"response_history": response_history}
        #print("\n---->" + json.dumps(response))
        return(response)

    return(ser)
    