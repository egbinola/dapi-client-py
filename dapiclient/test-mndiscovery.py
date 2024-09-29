import json
import time
from rpc.jsonrpc.jsonrpc_client import JsonRpcClient
from MNDiscovery.masternode_discovery import MasternodeDiscovery

def main():
    mnd = MasternodeDiscovery()
    print('Test - Get MN List')
    mnl = mnd.get_mnlist()
    print('Result: {} masternodes returned'.format(len(mnl)))

    print('Test - Random Node: {}'.format(mnd.get_random_masternode()))

    print('Test - Reset')
    mnd.reset()

    print('Test - Get MN List after reset')
    mnd.get_mnlist()

    print('Test - Get MN List before timeout')
    time.sleep(1)
    mnd.get_mnlist()

    print('Test - Try connecting to JSON-RPC on a MN')
    mnd.check_mn_response(mnl[0]['service'].split(':')[0])

    print('Test - Refresh list after timeout (60 seconds)')
    time.sleep(60)
    mnd.get_mnlist()
    print('Test - Complete')
    #print(json.dumps(mnl, indent = 2))

if __name__ == "__main__":
    main()
