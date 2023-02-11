import sys

sys.path.append( '..\custom_tests' )

from custom_test_mqtt import custom_test_mqtt_iterative

custom_test_mqtt_iterative(msg_length_start=10, msg_length_end=1010, msg_length_step_size=250, nbiot_connected = True, wait=False)
