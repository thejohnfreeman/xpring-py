import grpc
from xpring.proto.get_fee_request_pb2 import GetFeeRequest
from xpring.proto.get_account_info_request_pb2 import GetAccountInfoRequest
from xpring.proto.xrp_ledger_pb2_grpc import XRPLedgerStub


class XpringClient:

    def __init__(self, grpc_client: XRPLedgerStub):
        self.grpc_client = grpc_client

    @classmethod
    def from_endpoint(cls, grpc_url: str = 'grpc.xpring.tech:80'):
        channel = grpc.insecure_channel(grpc_url)
        grpc_client = XRPLedgerStub(channel)
        return cls(grpc_client)

    def get_account_info(self, address: str):
        request = GetAccountInfoRequest(address=address)
        return self.grpc_client.GetAccountInfo(request)

    def get_balance(self, address: str):
        account_info = self.get_account_info(address)
        return account_info.balance

    def get_fee(self):
        request = GetFeeRequest()
        return self.grpc_client.GetFee(request)
