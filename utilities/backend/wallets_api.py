from utilities.backend.backend_base import table, rpc
from utilities.consts import FUNCTIONS

__all__ = ["get_wallet_summary"]

def get_wallet_summary():
    wallet_summary = rpc(FUNCTIONS.WALLET_SUMMARY)
    return wallet_summary

def get_all_wallets():
    return "abc"