A very basic DAPI client. Only supports retrieving from some JSON-RPC and gRPC
endpoints. No validation of anything. No submitting of data, tx creation,
signing, etc.

# Quickstart


```
git clone https://github.com/thephez/dapi-client-py.git
cd dapi-client-py
python3 -m venv dapiclient-venv
source dapiclient-venv/bin/activate
pip install -r requirements.txt
python setup.py install

# Check masternode list
python dapiclient/test-mndiscovery.py

# Check DAPI client functionality
python dapiclient/test-dapiclient.py
```

# Examples


## Layer 1

```python
from client import DAPIClient

client = DAPIClient()

current_block_hash = client.getBestBlockHash()
print(current_block_hash)

height = 0
genesis_block_hash = client.getBlockHash(height)
print(genesis_block_hash)
```


## Layer 2

```python
from client import DAPIClient
import cbor2

client = DAPIClient()

id = client.getIdentity('Bb2p582MFR1tQhVQHKrScsAJH6Erqsb6SoroD9dQhJ5e')
print(id)

# Retrieve DPNS contract
contract = client.getDataContract('2KfMcMxktKimJxAZUeZwYkFUsEcAZhDKEpQs8GMnpUse')
print(contract)

# Retrieve 5 domain names from DPNS
docs = client.getDocuments(
    '2KfMcMxktKimJxAZUeZwYkFUsEcAZhDKEpQs8GMnpUse',
    'domain',
    limit=5,
    start_at=2
)
print('{} documents retrieved'.format(len(docs)))
for doc in docs:
    print('Document:\n\t{}\n'.format(cbor2.loads(doc)))
```
