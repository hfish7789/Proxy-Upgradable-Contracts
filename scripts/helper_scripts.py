import eth_utils
from web3.main import Web3
from brownie import config, network, accounts, Contract, interface



LOCAL_BLOCKCHAINS = ["ganache-local", "development"]

FORKED_BLOCHCHAINS = ["mainnet-fork", "mainnet-fork-dev"]

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


def get_account(index=None):
    if (
        network.show_active() in LOCAL_BLOCKCHAINS
        or network.show_active() in FORKED_BLOCHCHAINS
    ):
        if index is not None:
            return accounts[index]
        else:
            return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def toWei(amount):
    return Web3.toWei(amount, "ether")


def fromWei(amount):
    return Web3.fromWei(amount, "ether")
 
def get_contract(_contract, contract_address):
    contract = Contract.from_abi(_contract._name, contract_address, _contract.abi)
    return contract

def encode_data(initializer=None, *args):
    if len(args) == 0 or initializer is None:
        return eth_utils.to_bytes(hexstr="0x")
    return initializer.encode_input(*args)
