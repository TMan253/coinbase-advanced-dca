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

### Runtime setup for FreeBSD
Use the following steps to deploy on a FreeBSD host:
1. su - root
2. pkg update -f
3. pkg install git
3. pkg install python
4. python -V  # Assuming this return v3.9, then:
5. pkg install py39-pip
6. curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
7. vi .cshrc
8. Append the following to the PATH export: `$HOME/.cargo/bin`
9. su - dca   # Assuming service account 'dca'
10. Append the following to the PATH export: `/root/.cargo/bin`
11. Log out and log back in to source the new PATH.
12. mkdir /coinbase-advanced-dca
13. chown dca:dca /coinbase-advanced-dca
14. su - dca
15. ln -s /coinbase-advanced-dca coinbase-advanced-dca
16. rustup default stable
17. git clone https://github.com/TMan253/coinbase-advanced-dca.git
18. cd coinbase-advanced-dca
19. python -m venv foo
20. . foo/bin/activate
21. pip --version
22. pip install --upgrade pip
23. pip --version
24. pip install coinbase-advanced-py
25. vi config.ini
26. Add the following contents, but substitute your API key and secret within the quotation marks, and then save the file and exit:
```
[API]
API Key = "yourKeyHere"
API Secret = "yourSecretHere"
```
27. python cb-adv-dca.py test -c BTC -f 100.00
28. mkdir logs
29. chmod 744 dca.sh
30. crontab -e
31. Add the following:
```
#
# Note:  For multi-value, use commas:  3,12,47
# Note:  For every X interval, use /:  */X
# Note:  Aliases:  @reboot = once at startup, @hourly
#
#
#    +--------- Minute (0-59)
#    |    +------- Hour (0-23)
#    |    |    +----- Day Of Month (1-31)
#    |    |    |    +--- Month (1 -12)
#    |    |    |    |    +- Day Of Week (0-6) (Sunday = 0)
#    |    |    |    |    |
#    *    *    *    *    *     COMMAND
#----+----+----+----+----+-----+------------------------------------------------
#    *    *    *    *    *     /coinbase-advanced-dca/dca.sh coinbase-advanced-dca/bin/activate "asdf" "me@example.com" "test -c b -f 100.00"
#    0   11    *    *    1     /coinbase-advanced-dca/dca.sh coinbase-advanced-dca/bin/activate "asdf" "me@example.com" "buy -c b -f 100.00"
#    0   11    *    *    1,4   /coinbase-advanced-dca/dca.sh coinbase-advanced-dca/bin/activate "asdf" "me@example.com" "buy -c b -f 100.00"
#    0   11    *    *    3     /coinbase-advanced-dca/dca.sh coinbase-advanced-dca/bin/activate "asdf" "me@example.com" "buy -c e -f 100.00"
#    0   11    *    *    3,6   /coinbase-advanced-dca/dca.sh coinbase-advanced-dca/bin/activate "asdf" "me@example.com" "buy -c e -f 100.00"
#    0   11    *    *    0     /coinbase-advanced-dca/dca.sh coinbase-advanced-dca/bin/activate "asdf" "me@example.com" "buy -c SEI-USD -f 50.00"
#    0   11    *    *    2     /coinbase-advanced-dca/dca.sh coinbase-advanced-dca/bin/activate "asdf" "me@example.com" "buy -c s -f 100.00"
#    0   11    *    *    5     /coinbase-advanced-dca/dca.sh coinbase-advanced-dca/bin/activate "asdf" "me@example.com" "buy -c SUI-USD -f 50.00"
#    1   11    *    *    5     /coinbase-advanced-dca/dca.sh coinbase-advanced-dca/bin/activate "asdf" "me@example.com" "buy -c TIA-USD -f 50.00"
#    *    *    *    *    *     /coinbase-advanced-dca/dca.sh coinbase-advanced-dca/bin/activate "asdf" "me@example.com" "view"
#
#
```

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
