import sys

sys.path.append( '..\custom_tests' )

from custom_test_CSQ import custom_test_acquire_signal_quality_with_network_information

custom_test_acquire_signal_quality_with_network_information(s_of_delay=1, activate_gnss=False)
