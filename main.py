import requests
import json

import yfinance as yf


def load_addresses() -> list:
    # Load all addresses in address.txt
    with open('address.txt', 'r') as file:
        return file.read().split()


def get_address_balance(address: str, return_btc: bool=False, return_eur: bool=False) -> float:
    # Return address' balance for an account in satoshis (default), bitcoin or eur.
    r       = requests.get(f"https://blockchain.info/rawaddr/{address}")
    data    = json.loads(r.text)

    if not 'final_balance' in data.keys():
        raise ValueError("'address' is not valid or have not been found")

    balance = data['final_balance']

    if return_btc:
        return balance/1e8

    if return_eur:
        btc_value = yf.Ticker('BTC-EUR').history(period='1d')['Close'][0]
        return balance*btc_value/1e8
    
    return balance


def get_total_balance(return_btc: bool=False, return_eur: bool=False) -> float:
    # Get total balance for all addresses in address.txt
    balance = 0
    for address in load_addresses():
        balance += get_address_balance(address, return_btc, return_eur)
    return balance


if __name__ == '__main__':
    print(get_total_balance(return_eur=True))