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
from xpring.types import (
    Address,
    Amount,
    DigestLike,
    SignedTransaction,
    TransactionStatus,
    to_digest,
)
from xpring.wallet import Wallet


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

    def get_balance(self, address: Address) -> int:
        account = self.get_account(address)
        return account.account_data.balance.value.xrp_amount.drops

    def get_fee(self) -> GetFeeResponse:
        request = GetFeeRequest()
        return self.grpc_client.GetFee(request)

    def submit(
        self, signed_transaction: SignedTransaction
    ) -> SubmitTransactionResponse:
        blob = serialize_transaction(signed_transaction)
        request = SubmitTransactionRequest(signed_transaction=blob)
        return self.grpc_client.SubmitTransaction(request)

    def send(
        self, wallet: Wallet, destination: Address, amount: Amount
    ) -> SignedTransaction:
        address = wallet.address
        account = self.get_account(address)
        fees = self.get_fee()
        unsigned_transaction = {
            'Account': address,
            'Amount': amount,
            'Destination': destination,
            'Fee': str(fees.fee.minimum_fee.drops),
            'Flags': 0x80000000,
            'Sequence': account.account_data.sequence.value,
            'TransactionType': 'Payment'
        }
        return wallet.sign_transaction(unsigned_transaction)

    def get_transaction(self, txid: DigestLike) -> GetTransactionResponse:
        txid = to_digest(txid)
        request = GetTransactionRequest(hash=txid)
        return self.grpc_client.GetTransaction(request)

    def get_transaction_status(self, txid: DigestLike) -> TransactionStatus:
        transaction = self.get_transaction(txid)
        if not transaction.validated:
            return TransactionStatus.PENDING
        return (
            TransactionStatus.SUCCEEDED
            if transaction.meta.transaction_result.result.startswith('tes') else
            TransactionStatus.FAILED
        )
