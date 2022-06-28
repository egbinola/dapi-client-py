import hashlib
import importlib
from logging import Handler
from dapiclient.client import DAPIClient
from thumbor.handlers.imaging import ImagingHandler
from thumbor_dash.error_handlers.sentry import ErrorHandler
from thumbor_dash.error_handlers import *

import cbor2
import base58
from hashlib import sha256
from binascii import hexlify, unhexlify


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
        return docs[0]# Return the only document in the list


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

# Test getIdentity
    id = base58.b58decode("856aSH6uEBaHpndZYXDk72NJbZqXokNSPGrs8nKbd7QL")
    identity = getIdentity(id=id, prove=False, seed_ip='seed-1.testnet.networks.dash.org', mn_ip=None)
    print("Test getIdentity", str(identity))

# Tet getDataContract
    contract_id = base58.b58decode("EC7HZ6itSLiCmYsdR1gnqkxP1UWEaruQR2zdERHhgNfW")
    data_contract = getDataContract(contract_id=contract_id, prove=False, seed_ip='seed-1.testnet.networks.dash.org', mn_ip=None)
    print ("Test getDataContract", str(data_contract))

# Test getDocuments
    data = {
        'contract_id': base58.b58decode('EC7HZ6itSLiCmYsdR1gnqkxP1UWEaruQR2zdERHhgNfW'),
        'document_type': 'note',
        'where': b''
    }
    docs = getDocuments(handler=ErrorHandler,data=data,prove=False, seed_ip='seed-1.testnet.networks.dash.org', mn_ip=None)    
    print("Test getDocuments", str(docs))

# Test getIdentitiesByPublicKeyHashes
    public_key = b'''{
      'id': 0,
      'type': 0,
      'purpose': 0,
      'securityLevel': 0,
      'data': 'AxC5a+d0ocvhrdl+j86JF6aDpUY7TQG1t6ujvS6pYZjk',
      'readOnly': False,
    }'''
    public_key_hash = sha256(sha256(public_key).digest()).digest()
    public_key_hashes = [public_key_hash]
    identities = getIdentitiesByPublicKeyHashes(public_key_hashes=public_key_hashes, prove=False, seed_ip='seed-1.testnet.networks.dash.org', mn_ip=None)
    print("Test getIdentitiesByPublicKeyHashes", str(identities))

# Test getIdentityIdsByPublicKeyHashes
    public_key = b'''{
      'id': 0,
      'type': 0,
      'purpose': 0,
      'securityLevel': 0,
      'data': 'AxC5a+d0ocvhrdl+j86JF6aDpUY7TQG1t6ujvS6pYZjk',
      'readOnly': False,
    }'''
    public_key_hash = sha256(sha256(public_key).digest()).digest()
    public_key_hashes = [public_key_hash]
    identities = getIdentityIdsByPublicKeyHashes(public_key_hashes=public_key_hashes, prove=False, seed_ip='seed-1.testnet.networks.dash.org', mn_ip=None)
    print("Test getIdentityIdsByPublicKeyHashes", str(identities))

   
if __name__ == "__main__":
    main()




