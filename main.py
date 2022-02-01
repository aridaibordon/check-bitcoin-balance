import requests
import json


def check_address_balance(address: str, return_in_satoshis: bool=False) -> float:
    # Return address' balance for an account in bitcoin (default) or in satoshis.
    r       = requests.get(f"https://blockchain.info/rawaddr/{address}")
    data    = json.loads(r.text)

    if "final_balance" in data.keys():
        balance = data['final_balance'] if return_in_satoshis else data['final_balance']/1e8
        return balance
    raise ValueError("'address' is not valid or have not been found")
