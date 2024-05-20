# coinbase-advanced-dca
A tool for making a $100 BTC-USD market purchase on Coinbase Pro. The $100 purchase can be automated on Coinbase retail for $2.99 per trade. Alternatively, this tool allows the same dollar-cost averaging to be done on Coinbase Advanced for $0.55 per trade. "Very save! WOW. Much nice!"

## Disclaimer
Thanks for using cb-adv-dca.py at your own risk! :)

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

### Docker dev environment setup
Use the following steps to create a local development environment:
1. python -m venv foo
2. source foo/bin/activate   # for Linux, or for Windows:  foo\Scripts\activate
3. pip3 install coinbase-advanced-py
4. ?