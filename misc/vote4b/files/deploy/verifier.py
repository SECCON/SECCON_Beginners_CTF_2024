#!/usr/bin/env python3
# Kindly copied from Dreamhack :)
from web3 import Web3
import os

ABI = [
    {
        "type": "function",
        "name": "isSolved",
        "inputs": [],
        "outputs": [{"name": "", "type": "uint"}],
        "stateMutability": "view",
    }
]

rpc_url = os.environ["RPC_URL"]
contract_address = os.environ["LEVEL_CONTRACT_ADDRESS"]


def verify():
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    assert w3.is_connected(), "RPC server must be connectable"

    contract = w3.eth.contract(address=contract_address, abi=ABI)
    return contract.functions.isSolved().call() == 1


if __name__ == "__main__":
    if verify():
        exit(0)
    exit(1)
