import requests
import json
import time

import yfinance as yf

from bitcoin_balance.private import get_public_address_from_private_key

ADDRESS_FILENAME = 'address.txt'


def load_addresses(filename: str = ADDRESS_FILENAME) -> list:
    """Load addresses on ADDRESS_FILENAME"""
    try:
        with open('address.txt', 'r') as file:
            return file.read().split()
    except FileNotFoundError as e:
        print(f"{ADDRESS_FILENAME} has not been created yet.")
        return []


def add_address(address, filename: str = ADDRESS_FILENAME) -> None:
    """Add address to ADDRESS_FILENAME"""
    with open(ADDRESS_FILENAME, 'r') as file:
        file.write(address)


def get_address_balance(address: str,
                        return_btc: bool = False,
                        return_dol: bool = False,
                        private_key: bool = False) -> float:
    """Return balance for a given BTC address"""
    r = requests.get(f"https://blockchain.info/rawaddr/{address}")
    data = json.loads(r.text)

    if not 'final_balance' in data.keys():
        raise ValueError(
            f"'address' {address} is not valid or have not been found")
    
    if private_key:
        address = get_public_address_from_private_key(address)

    balance = data['final_balance'] / 1e8 if return_btc else data[
        'final_balance']

    if return_dol:
        btc_value = yf.Ticker('BTC-USD').history(period='1d')['Close'][0]
        return balance * btc_value / 1e8

    return balance


def get_total_balance(return_sum: bool = True, **kwargs) -> float:
    """Return total balance of all addresses in ADDRESS_FILENAME"""
    balance = {}
    for address in load_addresses():
        balance[address] = get_address_balance(address, **kwargs)
        time.sleep(1)

    if return_sum:
        return sum(balance.values())
    return balance
