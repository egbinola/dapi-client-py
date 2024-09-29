from dapiclient.client import DAPIClient

client = DAPIClient()


def jsonrpc_tests():
    current_block_hash = client.getBestBlockHash()
    print('Test - getBestBlockHash: {}\n'.format(current_block_hash))

    height = 0
    genesis_block_hash = client.getBlockHash(height)
    print('Test - getBlockHash (height: {}): {}\n'.format(height, genesis_block_hash))

    # mnlist_diff = client.getMnListDiff(genesis_block_hash, current_block_hash)
    # print('Test - getMnListDiff:\n{}\n'.format(mnlist_diff))

    # utxo = client.getUTXO('yPprxZrUL8UN73qLDS2xCg6yBFGieUWz7Q')#, 2)
    # print('Test - getUTXO:\n{}\n'.format(utxo))

    # address = 'yVs4HGmHgzP4t3gZ7KrpxRzCmkQcvZmczd'
    # getAddressSummary = client.getAddressSummary(address)
    # print('Test - getAddressSummary (address: {}): {}\n' .format(address, getAddressSummary))
    # return mnlist_diff

def jsonrpc_comm_test(mnlist_diff):
    print('Test - Check for JSON-RPC response from all masternodes')
    for mn in mnlist_diff['mnList']:
        ip = mn['service'].split(':')[0]
        try:
            response = client.make_request_to_node('getBestBlockHash', {}, ip)
            print('Successful response from {}: {}'.format(ip, response))
        except Exception as ex:
            print('*** Failure from {} ***'.format(ip))


def main():
    mnlist_diff = jsonrpc_tests()

    # jsonrpc_comm_test(mnlist_diff)


if __name__ == "__main__":
    main()