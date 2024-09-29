import hashlib
import importlib
import random
from logging import Handler
from dapiclient.client import DAPIClient
# from thumbor.handlers.imaging import ImagingHandler
# from thumbor_dash.error_handlers.sentry import ErrorHandler
# from thumbor_dash.error_handlers import *

import base58
from hashlib import sha256
from binascii import hexlify, unhexlify
from dapiclient.MNDiscovery import DAPI_ADDRESSES_WHITELIST


def getIdentity(id, prove, seed_ip = None, mn_ip = None):
    client = DAPIClient(seed_ip=seed_ip, mn_ip = mn_ip)

    try:
        identity = client.getIdentity(id=id, prove=prove)
    except Exception as e:
        return e
    else:   
        return identity # Return the identity


def getDataContract(contract_id, prove, seed_ip = None, mn_ip = None):
    client = DAPIClient(seed_ip=seed_ip, mn_ip = mn_ip)

    try:
        data_contract = client.getDataContract(id=contract_id, prove=prove)
    except Exception as e:
        return e
    else:   
        return data_contract # Return the data contract


def getDocuments(handler, data, prove, seed_ip = None, mn_ip = None):
    client = DAPIClient(seed_ip=seed_ip, mn_ip = mn_ip)

    try:
        docs = client.getDocuments(
            data_contract_id=data['contract_id'],
            document_type=data['document_type'],
            prove=prove,
            where=data['where'],
            limit=2,     
        )
    except Exception as e:
        return e
    else:
        return docs


def getIdentitiesByPublicKeyHashes(public_key_hashes, prove, seed_ip = None, mn_ip = None):
    client = DAPIClient(seed_ip=seed_ip, mn_ip = mn_ip)

    try:
        data_contract = client.getIdentitiesByPublicKeyHashes(public_key_hashes=public_key_hashes, prove=prove)
    except Exception as e:
        return e
    else:   
        return data_contract # Return the data contract


def getIdentityIdsByPublicKeyHashes(public_key_hashes, prove, seed_ip = None, mn_ip = None):
    client = DAPIClient(seed_ip=seed_ip, mn_ip = mn_ip)

    try:
        data_contract = client.getIdentityIdsByPublicKeyHashes(public_key_hashes=public_key_hashes, prove=prove)
    except Exception as e:
        return e
    else:   
        return data_contract # Return the data contract




def main():
    CONTRACT_ID = "GWRSAVFMjXx8HpQFaNJMqBV7MBgMK4br5UESsB4S31Ec"

    # Test getIdentity
    id = base58.b58decode("GgZekwh38XcWQTyWWWvmw6CEYFnLU7yiZFPWZEjqKHit")
    identity = getIdentity(id=id, prove=False)
    print("Test getIdentity", str(identity))

    # Test getDataContract
    contract_id = base58.b58decode(CONTRACT_ID)
    data_contract = getDataContract(contract_id=contract_id, prove=False, seed_ip=None, mn_ip=None)
    print ("Test getDataContract", str(data_contract))

    # Test getDocuments
    data = {
        'contract_id': base58.b58decode(CONTRACT_ID),
        'document_type': 'domain',
        'where': b''
    }
    docs = getDocuments(handler=Handler,data=data,prove=False, seed_ip=None, mn_ip=None)    
    print("Test getDocuments", docs)

   
if __name__ == "__main__":
    main()



