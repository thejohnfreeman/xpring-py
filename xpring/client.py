from dataclasses import dataclass

import grpc
from xpring.proto.v1.get_account_info_pb2 import (
    GetAccountInfoRequest,
    GetAccountInfoResponse,
)
from xpring.proto.v1.account_pb2 import AccountAddress
from xpring.proto.v1.get_fee_pb2 import (
    GetFeeRequest,
    GetFeeResponse,
)
from xpring.proto.v1.get_transaction_pb2 import (
    GetTransactionRequest,
    GetTransactionResponse,
)
from xpring.proto.v1.submit_pb2 import (
    SubmitTransactionRequest,
    SubmitTransactionResponse,
)
from xpring.proto.v1.xrp_ledger_pb2_grpc import XRPLedgerAPIServiceStub
from xpring.serialization import serialize_transaction
from xpring.types import Address, SignedTransaction


class Client:

    def __init__(self, grpc_client: XRPLedgerAPIServiceStub):
        self.grpc_client = grpc_client

    @classmethod
    def from_url(cls, grpc_url: str = 'grpc.xpring.tech:80'):
        channel = grpc.insecure_channel(grpc_url)
        grpc_client = XRPLedgerAPIServiceStub(channel)
        return cls(grpc_client)

    def get_account(self, address: Address) -> GetAccountInfoResponse:
        request = GetAccountInfoRequest(account=AccountAddress(address=address))
        return self.grpc_client.GetAccountInfo(request)

    def get_fee(self) -> GetFeeResponse:
        request = GetFeeRequest()
        return self.grpc_client.GetFee(request)

    def submit(
        self, signed_transaction: SignedTransaction
    ) -> SubmitTransactionResponse:
        blob = serialize_transaction(signed_transaction)
        request = SubmitTransactionRequest(signed_transaction=blob)
        return self.grpc_client.SubmitTransaction(request)

    def get_transaction(self, txid: bytes) -> GetTransactionResponse:
        request = GetTransactionRequest(hash=txid)
        return self.grpc_client.GetTransaction(request)
