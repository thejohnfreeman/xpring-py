from dataclasses import dataclass

import grpc
from xpring.proto.account_info_pb2 import AccountInfo
from xpring.proto.get_fee_request_pb2 import GetFeeRequest
from xpring.proto.get_account_info_request_pb2 import GetAccountInfoRequest
from xpring.proto.xrp_ledger_pb2_grpc import XRPLedgerAPIStub


@dataclass
class Account:
    balance: int
    sequence: int
    previous_txn_id: str
    previous_txn_lgr_seq: int


class Client:

    def __init__(self, grpc_client: XRPLedgerAPIStub):
        self.grpc_client = grpc_client

    @classmethod
    def from_url(cls, grpc_url: str = 'grpc.xpring.tech:80'):
        channel = grpc.insecure_channel(grpc_url)
        grpc_client = XRPLedgerAPIStub(channel)
        return cls(grpc_client)

    def _get_account_info(self, address: str) -> AccountInfo:
        request = GetAccountInfoRequest(address=address)
        return self.grpc_client.GetAccountInfo(request)

    def get_account_info(self, address: str) -> Account:
        response = self._get_account_info(address)
        return Account(
            int(response.balance.drops),
            int(response.sequence),
            response.previous_affecting_transaction_id,
            int(response.previous_affecting_transaction_ledger_version),
        )

    def get_balance(self, address: str) -> int:
        response = self._get_account_info(address)
        return int(response.balance.drops)

    def get_fee(self) -> int:
        request = GetFeeRequest()
        return int(self.grpc_client.GetFee(request).amount.drops)
