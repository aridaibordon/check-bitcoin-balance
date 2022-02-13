# Check bitcoin balance
Bitcoin balance checker using blockchain API.

This repository contains useful code to check the balance of a single or a collection of BTC addresses in satoshis, bitcoin or euros.

## Getting the data

It is possible to access any individual bitcoin address using the [get_address_balance](main.py) function.

To access the total balance of a group of accounts, add them to address.txt manually or use the [add_address](main.py) function and then use the [get_total_balance](main.py) function.

By default, [get_total_balance](main.py) returns the sum of all the balance in address.txt. To get individual information for each address in the form of a dictionary, set `return_sum` to False.

### Output format

By default, the output format of the balance is given in satoshis. Using the booleans `return_btc` and `return_eur` (which are set to False by default) alter this output:

* If `return_eur` is set to True: The output will be given in euros. Conversion rate is imported using yfinance.
* If `return_btc` is set to True: The output will be given in bitcoins (1 BTC = 1e8 satoshis).
