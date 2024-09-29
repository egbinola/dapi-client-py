import random
import datetime
from dapiclient.rpc.jsonrpc.jsonrpc_client import JsonRpcClient

# TODO: Stop using hard-coded seed in all requests
SEED_IP = 'seed-1.testnet.networks.dash.org'
SEED_PORT = 3000
MN_LIST_UPDATE_INTERVAL = 60000 / 1000



'''
 * This class holds the valid deterministic masternode list
 * @type {SimplifiedMNListEntry[]}
 * @property {string} proRegTxHash
 * @property {string} confirmedHash
 * @property {string} service - ip and port
 * @property {string} pubKeyOperator - operator public key
 * @property {string} keyIDVoting - public key hash, 20 bytes
 * @property {boolean} isValid
'''
class SimplifiedMNListEntry:
    def __init__(self, seeds, dapi_port = 3000):
        #self.mn_service = set()
        self.mn_entry = []

    def add_entry(self, entry):
        self.mn_entry.append(entry)

    #def add_service(self, service):
    #    self.mn_service.add(service)

    def get_random_masternode(self):
        return random.sample(self.mn_entry, 1)[0]['service']

class MasternodeListProvider:
    def __init__(self, seeds, dapi_port = SEED_PORT):
        self.SEED_IP = seeds
        if seeds is None:
            seeds = SEED_IP
        if dapi_port is None:
            dapi_port = SEED_PORT

        self.masternode_list = []
        #self.simplified_masternode_list = SimplifiedMNList()
        self.dapi_port = dapi_port
        self.last_update_date = 0
        self.base_block_hash = '0000000000000000000000000000000000000000000000000000000000000000' #constants.masternodeList.NULL_HASH;

    def isEmptyMasternodeList(self):
        return True if len(self.masternode_list.length) == 0 else False


    def get_genesis_hash(self):
        genesis_height = 0
        #node = self.isEmptyMasternodeList() ? sample(self.seeds) : sample(self.masternodeList);
        #ip_address = node.service.split(':')[0];
        ip_address = self.SEED_IP

        genesis_block_hash = JsonRpcClient.request({
            'host': ip_address,
            'port': self.dapi_port
        }, 'getBlockHash', { 'height': genesis_height })
        return genesis_block_hash


    def update_mn_list(self):
    #if (self.base_block_hash === config.nullHash) {
        self.base_block_hash = self.get_genesis_hash()
        diff = self.get_simplified_mn_list_diff()

        #self.masternode_list = validMasternodesList;
        self.masternode_list = diff['mnList']
        self.base_block_hash = diff['baseBlockHash']
        self.last_update_date = datetime.datetime.utcnow().timestamp()


    def get_simplified_mn_list_diff(self):
        #node = this.isEmptyMasternodeList() ? sample(this.seeds) : sample(this.masternodeList);
        base_block_hash = self.base_block_hash;
        ip_address =  self.SEED_IP #node.service.split(':')[0];

        block_hash = JsonRpcClient.request({
            'host': ip_address,
            'port': self.dapi_port
        }, 'getBestBlockHash')

        # TODO: error checking on blockhash response

        #if (!blockHash) {
        #  throw new Error(`Failed to get best block hash for getSimplifiedMNListDiff from node ${ipAddress}`);
        #}

        params = {
            'baseBlockHash': base_block_hash,
            'blockHash': block_hash
        }
        diff = JsonRpcClient.request({
            'host': ip_address,
            'port': self.dapi_port
        }, 'getMnListDiff', params)

        # TODO: error checking on diff response

        #if (!diff) {
        #  throw new Error(`Failed to get mn diff from node ${ipAddress}`);
        #}
        return diff


    def needs_update(self):
        time_since_update = datetime.datetime.utcnow().timestamp() - self.last_update_date #MN_LIST_UPDATE_INTERVAL
        #print('Time since update: {}; Limit: {}'.format(time_since_update, MN_LIST_UPDATE_INTERVAL))
        return True if time_since_update > MN_LIST_UPDATE_INTERVAL else False


    def get_mn_list(self):
        if (self.needs_update()):
            #print('Masternode List needs updating...')
            self.update_mn_list()

        return self.masternode_list


    def check_mn_response(self, ip_address):
        try:
            block_hash = JsonRpcClient.request({
                'host': ip_address,
                'port': self.dapi_port
            }, 'getBestBlockHash')
            print('Success from {}:\t{}'.format(ip_address, block_hash))
        except Exception as ex:
            print('Failure from {}:\t** {} **'.format(ip_address, ex))


def main():
    mnlist_provider = MasternodeListProvider(None)
    masternode_list = mnlist_provider.get_mn_list()

    print('Masternode list contain {} masternodes'.format(len(masternode_list)))

    print('Checking JSON-RPC response from all masternodes')
    for m in masternode_list:
        mnlist_provider.check_mn_response(m['service'].split(':')[0])
    return

if __name__ == "__main__":
    main()