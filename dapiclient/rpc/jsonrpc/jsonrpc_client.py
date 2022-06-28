import requests
import json

RPC_VERSION = '2.0'

class JsonRpcClient:

    def __init__(self):
        return


    def request(url, method, params = {}, options = {}):
        #print(url)
        destination = 'http://{}:{}'.format(url['host'], url['port'])

        payload = {
            'jsonrpc': RPC_VERSION,
            'method': method,
            'params': params,
            'id': 1
            }

        headers = {'content-type': 'application/json'}

        try:
            response = requests.post(destination, data=json.dumps(payload), headers=headers, timeout=50000)
            response.raise_for_status()

            parsed = json.loads(response.text)
            print("Parsed response", parsed)
            #print('{} response:\n{}\n\n'.format(method, json.dumps(parsed, indent=4, sort_keys=True)))
            if 'result' in parsed:
                return parsed['result']
            elif 'error' in parsed:
                return parsed['error']

        except Exception as ex:
            print('Exception for {} - {}\n\t{}'.format(url, payload, ex))
            raise
