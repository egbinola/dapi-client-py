from dapiclient.MNDiscovery import DAPI_ADDRESSES_WHITELIST
from .masternode_list_provider import MasternodeListProvider
import random

class MasternodeDiscovery:
    def __init__(self, seeds = None, port = None):
        self.mnlist_provider = MasternodeListProvider(seeds, port)
        self.seeds = seeds


    def get_random_masternode(self, excluded_ips = None):
        mnlist = self.mnlist_provider.get_mn_list()
        ip_list = []
        for mn in mnlist:
            current_mn_ip = mn['service'].split(":")[0]
            ip_list.append(current_mn_ip)
        
        checked_ip_list = []

        for ip in ip_list:
            if ip in DAPI_ADDRESSES_WHITELIST:
                checked_ip_list.append(ip) 
        return random.choice(checked_ip_list)

    def get_mnlist(self):
        return self.mnlist_provider.get_mn_list()


    def check_mn_response(self, ip_address):
        return self.mnlist_provider.check_mn_response(ip_address)


    def reset(self):
        self.mnlist_provider = MasternodeListProvider(self.seeds);