import sys
sys.path.append( '..' )

import json

def print_cmd_history(cmd_history):
    for cmd_response in cmd_history['response_history']:
        response = json.dumps(cmd_response).encode('utf8')
        print(response.decode())