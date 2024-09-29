import grpc
import cbor2

# Generated from dapi-grpc
import dapiclient.rpc.grpc.core_pb2 as core_pb2
import dapiclient.rpc.grpc.core_pb2_grpc as core_pb2_grpc
import dapiclient.rpc.grpc.platform_pb2 as platform_pb2
import dapiclient.rpc.grpc.platform_pb2_grpc as platform_pb2_grpc


class GRpcClient:

    def __init__(self):
        pass

    def request(socket, method, params = {}, options = {'timeout': 5000}):
        # Create insecure credentials that don't validate the server certificate
        credentials = grpc.ssl_channel_credentials(root_certificates=None)
        channel = grpc.secure_channel(
            socket,  # e.g., 'yourserver.com:443'
            credentials,
            options=(('grpc.enable_http_proxy', 0),))
       
        # print('socket: {}'.format(socket))

        stub = platform_pb2_grpc.PlatformStub(channel)
        stubCore = core_pb2_grpc.CoreStub(channel)

        if method == 'getIdentity':
            return GRpcClient.getIdentity(stub, params, options)

        elif method == 'getDataContract':
            return GRpcClient.getDataContract(stub, params, options)

        elif method == 'getDocuments':
            return GRpcClient.getDocuments(stub, params, options)

        elif method == 'getIdentitiesByPublicKeyHashes':
            return GRpcClient.getIdentitiesByPublicKeyHashes(stub, params, options)

        elif method == 'getIdentityIdsByPublicKeyHashes':
            return GRpcClient.getIdentityIdsByPublicKeyHashes(stub, params, options)

        elif method == 'waitForStateTransitionResult':
            return GRpcClient.waitForStateTransitionResult(stub, params, options)

        elif method == 'getBlock':
            return GRpcClient.getBlock(stubCore, params, options)

        elif method == 'getStatus':
            return GRpcClient.getStatus(stubCore, params, options)

        elif method == 'getTransaction':
            return GRpcClient.getTransaction(stubCore, params, options)

        elif method == 'sendTransaction':
            return GRpcClient.sendTransaction(stubCore, params, options)

        elif method == 'subscribeToTransactionsWithProofs':
            return GRpcClient.subscribeToTransactionsWithProofs(stubCore, params, options)

        else:
            raise ValueError('Unknown gRPC endpoint: {}'.format(method))


    def getIdentity(stub, params, options):
        # Create Identity request
        identity_request_v0 = platform_pb2.GetIdentityRequest.GetIdentityRequestV0()

        # Set identity parameter of request
        identity_request_v0.id = params['id'] 
        identity_request_v0.prove = params['prove']

        # Create GetIdentityRequest instance and set version v0 to identity_request_v0
        identity_request = platform_pb2.GetIdentityRequest()
        identity_request.v0.CopyFrom(identity_request_v0)

        response = stub.getIdentity(identity_request, options['timeout'])
        responseBytes = bytearray(response.v0.identity)
        # identityBytes = responseBytes[4 : len(responseBytes)]
        # return cbor2.loads(identityBytes)
        return responseBytes

    def getDataContract(stub, params, options):
        # Create a version-specific GetDataContractRequestV0 message
        contract_request_v0 = platform_pb2.GetDataContractRequest.GetDataContractRequestV0()
        contract_request_v0.id = params['id']
        contract_request_v0.prove = params['prove']

        # Create the GetDataContractRequest message and set the v0 field
        contract_request = platform_pb2.GetDataContractRequest()
        contract_request.v0.CopyFrom(contract_request_v0)

        # Send the request and receive the response
        response = stub.getDataContract(contract_request, options['timeout'])
        return response.v0.data_contract


    def getDocuments(stub, params, options):
        # Create the version-specific GetDocumentsRequestV0 message
        document_request_v0 = platform_pb2.GetDocumentsRequest.GetDocumentsRequestV0()

        # Set required fields
        document_request_v0.data_contract_id = params['data_contract_id']
        document_request_v0.document_type = params['document_type']
        
        # Check and set optional fields if present in params
        if params.get('where'):
            document_request_v0.where = params['where']
            
        if params.get('order_by'):
            document_request_v0.order_by = params['order_by']
            
        if params.get('limit') is not None:
            document_request_v0.limit = params['limit']
        
        # Handle oneof start (either start_at or start_after)
        if params.get('start_after'):
            document_request_v0.start_after = params['start_after']
        elif params.get('start_at'):
            document_request_v0.start_at = params['start_at']

        document_request_v0.prove = params['prove']

        # Create the GetDocumentsRequest message and set the v0 field
        document_request = platform_pb2.GetDocumentsRequest()
        document_request.v0.CopyFrom(document_request_v0)

        # Send the request and receive the response
        response = stub.getDocuments(document_request, options['timeout'])
        # print(response)
        return response.v0.documents

    def getBlock(stubCore, params, options):
        block_request = core_pb2.GetBlockRequest()
        block_request.hash = params['hash']
        block_request.height = params['height']

        response = stubCore.getBlock(block_request, options['timeout'])
        return cbor2.loads(response.block)

    def getStatus(stubCore, params, options):
        status_request = core_pb2.GetStatusRequest()

        response = stubCore.getStatus(status_request, options['timeout'])

        return response

    def getTransaction(stubCore, params, options):
        transaction_request = core_pb2.GetTransactionRequest()
        transaction_request.id = params['id']

        response = stubCore.getTransaction(transaction_request, options['timeout'])

        return response.transaction

    def sendTransaction(stubCore, params, options):
        transaction_request = core_pb2.SendTransactionRequest()
        transaction_request.transaction = params['transaction']
        transaction_request.allow_high_fees = params['allow_high_fees']
        transaction_request.bypass_limits = params['bypass_limits']

        response = stubCore.sendTransaction(transaction_request, options['timeout'])

        return response

    def subscribeToTransactionsWithProofs(stubTransactions, params, options):
        subscribe_request = core_pb2.TransactionsWithProofsRequest()
        subscribe_request.from_block_hash = params['from_block_hash']
        subscribe_request.from_block_height = params['from_block_height']
        subscribe_request.count = params['count']
        subscribe_request.send_transaction_hashes = params['send_transaction_hashes']
        setattr(subscribe_request.bloom_filter, 'n_hash_funcs', params['bloom_filter']['n_hash_funcs'])
        setattr(subscribe_request.bloom_filter, 'v_data', params['bloom_filter']['v_data'])
        setattr(subscribe_request.bloom_filter, 'n_tweak', params['bloom_filter']['n_tweak'])
        setattr(subscribe_request.bloom_filter, 'n_flags', params['bloom_filter']['n_flags'])

        response = stubTransactions.transactionWithProof(subscribe_request, options['timeout'])

        return response

    def getIdentitiesByPublicKeyHashes(stub, params, options):
        request = platform_pb2.GetIdentitiesByPublicKeyHashesRequest()
        request.public_key_hashes.extend(params['public_key_hashes'])
        request.prove = params['prove']

        response = stub.getIdentitiesByPublicKeyHashes(request, options['timeout'])

        return response

    def getIdentityIdsByPublicKeyHashes(stub, params, options):
        request = platform_pb2.GetIdentityIdsByPublicKeyHashesRequest()
        request.public_key_hashes.extend(params['public_key_hashes'])
        request.prove = params['prove']

        response = stub.getIdentityIdsByPublicKeyHashes(request, options['timeout'])

        return response

    
    def waitForStateTransitionResult(stub, params, options):
        request = platform_pb2.GetIdentityIdsByPublicKeyHashesRequest()
        request.state_transition_hash = params['state_transition_hash']
        request.prove = params['prove']

        response = stub.waitForStateTransitionResult(request, options['timeout'])

        return response