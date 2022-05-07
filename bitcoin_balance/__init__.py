import requests
import json

import yfinance as yf


def load_addresses() -> list:
    # load all addresses in address.txt
    with open('address.txt', 'r') as file:
        return file.read().split()


def add_address(address) -> None:
    # add new address to address.txt
    with open('address.txt', 'r') as file:
        file.write(address)


def get_address_balance(address: str, return_btc: bool=False, return_eur: bool=False) -> float:
    # return address' balance for an account in satoshis (default), bitcoin or eur.
    r       = requests.get(f"https://blockchain.info/rawaddr/{address}")
    data    = json.loads(r.text)

    if not 'final_balance' in data.keys():
        raise ValueError(f"'address' {address} is not valid or have not been found")

    balance = data['final_balance']/1e8 if return_btc else data['final_balance']

    if return_eur:
        btc_value = yf.Ticker('BTC-EUR').history(period='1d')['Close'][0]
        return balance*btc_value/1e8
    
    return balance


def get_total_balance(return_sum: bool=True, return_btc: bool=False, return_eur: bool=False) -> float:
    # get total balance for all addresses in address.txt
    balance = {}
    for address in load_addresses():
        balance[address] = get_address_balance(address, return_btc, return_eur)

    if return_sum:
        return sum(balance.values())
    return balance
