import random
import sys
from dapiclient.MNDiscovery.masternode_discovery import MasternodeDiscovery
from dapiclient.rpc.jsonrpc.jsonrpc_client import JsonRpcClient
from dapiclient.rpc.grpc.grpc_client import GRpcClient
from dapiclient.MNDiscovery import DAPI_ADDRESSES_WHITELIST


SEED_PORT = 1443
SEED_PORT_GRPC = 1443
GRPC_REQUEST_TIMEOUT = 50000
GRPC_MAX_RESULTS = 100


class DAPIClient:
    """docstring for DAPIClient."""

    def __init__(self, seed_ip = None,mn_ip = None, options = {}):
        # support user-defined seeds and ip
        self.mn_ip = mn_ip
        self.mn_discovery = MasternodeDiscovery(seeds=seed_ip) #options['seeds'], options['port'])
        self.dapi_port = SEED_PORT #if options.port not in options else options.port
        self.native_grpc_port = SEED_PORT_GRPC #options.nativeGrpcPort || config.grpc.nativePort;
        self.timeout = 2000 #options.timeout || 2000;
        #self.forceJsonRpc = options.forceJsonRpc;
        #preconditionsUtil.checkArgument(jsutil.isUnsignedInteger(self.timeout),
        #  'Expect timeout to be an unsigned integer');
        self.retries = 3 #options.retries ? options.retries : 3;
        #preconditionsUtil.checkArgument(jsutil.isUnsignedInteger(self.retries),
        #  'Expect retries to be an unsigned integer');
        #self.dpp = new DPP();
        #self.make_request = {}
        #self.make_request['call_count'] = 0

    def make_request_to_random_dapi_node(self, method, params = {}, excluded_ips = []):
        #self.make_request['call_count'] = 0;

        return self.make_request_with_retries(method, params, self.retries, excluded_ips)


    def make_request(self, method, params, excluded_ips = []):
        #print(method)
        #self.make_request['call_count'] += 1
        # random_masternode = self.mn_discovery.get_random_masternode(excluded_ips)
        random_masternode = random.choice(DAPI_ADDRESSES_WHITELIST)
        #print(random_masternode)
        return JsonRpcClient.request({
          'host': random_masternode.split(':')[0],
          'port': random_masternode.split(':')[1],
        }, method, params, { 'timeout': self.timeout }, False)


    def make_request_to_node(self, method, params, ip):
        return JsonRpcClient.request({
          'host': ip,
          'port': self.dapi_port,
        }, method, params, { 'timeout': self.timeout })


    def make_request_with_retries(self, method, params, retries_count, excluded_ips):
        try:
            return self.make_request(method, params, excluded_ips)
        except Exception as ex:
            print('Exception:\n{}'.format(ex))
            #if (err.code !== 'ECONNABORTED' && err.code !== 'ECONNREFUSED') {
            #throw err;
          #}
            if (retries_count > 0):
                print('*** Retrying ***')
                excluded_on_next_try = []
                #if (err.address) {
                #  excludedOnNextTry = Array.isArray(excludedIps)
                #    ? excludedIps.slice().push(err.address) : excludedOnNextTry.push(err.address);
                #}
                return self.make_request_with_retries(method, params, retries_count - 1, excluded_on_next_try)

            raise Exception('max retries to connect to DAPI node reached');

    def getAddressSummary(self, address):
        return self.make_request_to_random_dapi_node('getAddressSummary', {'address': [address]})

    def getBestBlockHash(self):
        return self.make_request_to_random_dapi_node('getBestBlockHash')


    def getBlockHash(self, height):
        return self.make_request_to_random_dapi_node('getBlockHash', {'height': height})


    def getMnListDiff(self, baseBlockHash, blockHash):
        return self.make_request_to_random_dapi_node('getMnListDiff',
            {
                'baseBlockHash': baseBlockHash,
                'blockHash': blockHash
            })


    def getUTXO(self, address, from_result=0, to_result=1000, fromHeight=0, toHeight=sys.maxsize):
        return self.make_request_to_random_dapi_node('getUTXO',
            {
                'address': address,
                'from': from_result,
                'to': to_result,
                'fromHeight': fromHeight,
                'toHeight': toHeight
            })

    # gRPC endpoints

    def make_request_to_random_dapi_grpc_node(self, method, retries_count, params = {}, options = {}, excluded_ips = []):
        #self.make_request['call_count'] = 0;
        if (self.mn_ip is None):
            #  random_masternode = self.mn_discovery.get_random_masternode()
             random_masternode = random.choice(DAPI_ADDRESSES_WHITELIST).split(':')[0]
             ip = random_masternode
        else:
             ip = self.mn_ip

        socket = '{}:{}'.format(ip, self.native_grpc_port)
        # socket = self.mn_ip
        options = {
            'timeout': GRPC_REQUEST_TIMEOUT
        }
        
        try:
            return GRpcClient.request(socket, method, params, options)
        except Exception as ex:
            print('Exception:\n{}'.format(ex))
            if (retries_count > 0):
                print('*** Retrying ***')
                excluded_on_next_try = []
                return self.make_request_to_random_dapi_grpc_node(method, retries_count - 1)

            raise Exception('max retries to connect to DAPI grpc node reached')

    def subscribeToTransactionsWithProofs(self, bloom_filter, from_block_hash, from_block_height, count=0, send_transaction_hashes=0):
        return self.make_request_to_random_dapi_grpc_node(
                'subscribeToTransactionsWithProofs',
                self.retries,
                {
                    'bloom_filter': bloom_filter,
                    'from_block_hash': from_block_hash,
                    'from_block_height': from_block_height,
                    'count': count,
                    'send_transaction_hashes': send_transaction_hashes
                }
        )

    def getBlock(self, hash=0, height=0):
        return self.make_request_to_random_dapi_grpc_node(
                'getBlock',
                self.retries,
                {
                    'hash': hash,
                    'height': height
                }
            )

    def getStatus(self):
        return self.make_request_to_random_dapi_grpc_node(
                'getStatus',
                self.retries,
        )

    def getTransaction(self, id):
        return self.make_request_to_random_dapi_grpc_node(
                'getTransaction',
                self.retries,
                {
                    'id': id
                }
        )

    def sendTransaction(self, transaction, allow_high_fees=0, bypass_limits=0):
        return self.make_request_to_random_dapi_grpc_node(
                'sendTransaction',
                self.retries,
                {
                    'transaction': transaction,
                    'allow_high_fees': allow_high_fees,
                    'bypass_limits': bypass_limits
                }
        )

    def getIdentity(self, id, prove):
        return self.make_request_to_random_dapi_grpc_node(
                'getIdentity',
                self.retries,
                {
                    'id': id,
                    'prove': prove,
                }
            )
    
    def getIdentityKeys(self, id, prove):
        return self.make_request_to_random_dapi_grpc_node(
                'getIdentityKeys',
                self.retries,
                {
                    'id': id,
                    'prove': prove,
                }
            )

    def getDataContract(self, id, prove):
        return self.make_request_to_random_dapi_grpc_node(
                'getDataContract', 
                self.retries,
                {
                    'id': id,
                    'prove': prove
                }
            )

    def getDocuments(self, data_contract_id, document_type, prove, start_at=b'', start_after=b'', where=b'', order_by=b'', limit=GRPC_MAX_RESULTS,):
        return self.make_request_to_random_dapi_grpc_node(
                'getDocuments', self.retries,
                {
                    'data_contract_id': data_contract_id,
                    'document_type': document_type,
                    'where': where,
                    'order_by': order_by,
                    'limit': limit,
                    'start_at': start_at,
                    'start_after': start_after,
                    'prove': prove,
                }
            )

    def getIdentitiesByPublicKeyHashes(self, public_key_hashes, prove):
        return self.make_request_to_random_dapi_grpc_node(
                'getIdentitiesByPublicKeyHashes',
                self.retries,
                {
                    'public_key_hashes': public_key_hashes,
                    'prove': prove
                }
            )

    def getIdentityIdsByPublicKeyHashes(self, public_key_hashes, prove):
        return self.make_request_to_random_dapi_grpc_node(
                'getIdentityIdsByPublicKeyHashes',
                self.retries,
                {
                    'public_key_hashes': public_key_hashes,
                    'prove': prove
                }
            )
            
    def waitForStateTransitionResult(self, state_transition_hash, prove):
        return self.make_request_to_random_dapi_grpc_node(
                'waitForStateTransitionResult',
                self.retries,
                {
                    'state_transition_hash': state_transition_hash,
                    'prove': prove
                }
            )

def main():
    client = DAPIClient()
    return

if __name__ == "__main__":
    main()