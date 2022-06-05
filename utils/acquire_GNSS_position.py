import sys
sys.path.append( '..' )

import serial
from serial_tools.send_cmd import send_cmd
from datetime import datetime
import json

'''
    Take care not to run it when WWAN is on as it would result in an error. To avoid WWAN (included nbiot) errors deactivate GNSS
'''
def acquire_GNSS_position(ser, retries=3): 
    print('acquire_signal_quality_report')

    for i in range(retries-1):
        cmd_response = send_cmd("AT+QGPSLOC=2", ser, print_final_response=False, ms_of_delay_before=1000*(i+1))
        print(cmd_response)

        response = cmd_response['response'][1][0:-2]
        status=cmd_response['status']
  
        is_error = response.split("ERROR: ")
        if len(is_error) != 1:
            error_number = is_error[1]
            if error_number != '516':

                cmd_response.status = 'ERROR' #just in this case at this moment because is displaying unfinished when 516 error(not fix position)
                return cmd_response
            else:
                print('\nGNSS position not fix (516 error) #' + str(i+1) + '\n')
        else:
            utc = response.split(':')[1].split(',')[0]
            lat = response.split(':')[1].split(',')[1]
            lat = lat.split('.')[0] +'.'+ lat.split('.')[1][1:]
            lng = response.split(':')[1].split(',')[2]
            lng = lng.split('.')[0] +'.'+ lng.split('.')[1][1:]
            hdop = response.split(':')[1].split(',')[3]
            altitude = response.split(':')[1].split(',')[4]
            fix = response.split(':')[1].split(',')[5]
            cog = response.split(':')[1].split(',')[6]
            spkm = response.split(':')[1].split(',')[7]
            spkn = response.split(':')[1].split(',')[8]
            date = response.split(':')[1].split(',')[9]
            nsat = response.split(':')[1].split(',')[10]
            
            readingTime = datetime.now()
            date=readingTime

            outDictionary = {
                'utc': utc,
                'lat': lat,
                'lng': lng,
                'hdop': hdop,
                'altitude': altitude,
                'fix': fix,
                'cog': cog,
                'spkm': spkm,
                'spkn': spkn,
                'date': date,
                'nsat': nsat,
                'status': status
            }

            print(outDictionary)
            print('\n\n')

            return outDictionary
    
    cmd_response['status'] = 'ERROR' #just in this case at this moment because is displaying unfinished when 516 error(not fix position)
    print('\nThird attempt - exiting\n\n')
    return cmd_response

def turn_on_GNSS(ser, GNSS_mode=1, accuracy="", fix_count="", fix_rate="", HEPE=""):
    
    cmd = "AT+QGPS=" + str(GNSS_mode) 
    if accuracy != '':
        cmd = cmd + "," + str(accuracy)
    if fix_count != '':
        cmd = cmd + "," + str(fix_count)
    if fix_rate != '':
        cmd = cmd + "," + str(fix_rate)
    if HEPE != '': #Accuracy threshold
        cmd = cmd + "," + str(HEPE)    
    cmd_response = send_cmd(cmd, ser,  print_final_response=True, ms_of_delay_after=10000) # check as error 504 returns unfinished instead of error
    
    print(cmd_response)
    print('\n')
    return(cmd_response)

def turn_off_GNSS(ser):
    
    cmd = "AT+QGPSEND"
    cmd_response = send_cmd(cmd, ser,  print_final_response=True, ms_of_delay_after=100) # check as error 504 returns unfinished instead of error
    
    print(cmd_response)
    print('\n')
    return(cmd_response)