# coinbase-advanced-dca
A tool for making a $100 BTC-USD market purchase on Coinbase Advanced. The $100 purchase can be automated on Coinbase retail for $2.99 per trade. Alternatively, this tool allows the same dollar-cost averaging to be done on Coinbase Advanced for $0.55 per trade. "Very save! WOW. Much nice!"

## Disclaimer
This tool is without guarantees or warranty and only available on an as is basis.  This tool is used at your own risk!

## Usage
```
usage: cb-adv-dca.py [-h] [-c COIN] [-f FUNDS] [-l LIMIT] [-d] [--version]
                     action

Buys digital assets on Coinbase Advanced.

options:
  -h, --help            show this help message and exit
  -d, --debug           toggle verbose logging
  --version             show program's version number and exit

configuring purchases:
  action                buy|test - live buy or simulation
  -c COIN, --coin COIN  the asset to purchase, such as b|e|s|BTC|ETH|SOL|BTC-   
                        USD. Default BTC-USD.
  -f FUNDS, --funds FUNDS
                        the amount to spend. Default 100.00.
  -l LIMIT, --limit LIMIT
                        0|1|5 - percent limit order discount. Default 0.0       
                        (market order).
```

## Creating an API key
This tool requires an API key for your Coinbase Advanced account.  To create an API key:
1. Log into https://portal.cdp.coinbase.com/access/api?keyType=trade
2. Click the `Create API key` button.
3. Name the key, choose the account it has access to, and enable `Trade` access.  Click `Create & download`.
4. Retain the key and secret in a safe manner because it is a bearer token that allows access to your account!

### Docker dev environment setup
`TBD`

### Dev environment setup
Use the following steps to create a local development environment:
1. git clone https://github.com/TMan253/coinbase-advanced-dca.git
2. cd coinbase-advanced-dca
3. python -m venv foo
4. source foo/bin/activate   # for Linux, or for Windows:  foo\Scripts\activate
5. pip3 install coinbase-advanced-py
6. notepad.exe .\config.ini
7. Add the following contents, but substitute your API key and secret within the quotation marks, and then save the file and exit:
```
[API]
API Key = "yourKeyHere"
API Secret = "yourSecretHere"
```
8. .\foo\Scripts\python.exe .\cb-adv-dca.py test -c BTC -f 100.00 -l 0.2
