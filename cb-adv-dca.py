# This file uses the Coinbase Advanced Python SDK
#   to invoke REST services for placing BUY side orders.
# See the Coinbase docs here:
#   - https://docs.cdp.coinbase.com/advanced-trade/docs/sdk-rest-client-trade/
#   - https://docs.cdp.coinbase.com/advanced-trade/reference/retailbrokerageapi_postorder/
#   - https://github.com/coinbase/coinbase-advanced-py/blob/master/coinbase/rest/orders.py#L333
#   - https://docs.cloud.coinbase.com/advanced-trade/docs/welcome

import configparser
from json import dumps
from coinbase.rest import RESTClient
import uuid
import math
import argparse

CONFIG_FILE="config.ini"
CONFIG=None
API_KEY=""
API_SECRET=""
ARGS=None
DEBUG=True
TEST_MODE=True
PRODUCT = "BTC-USD"
FUNDS = "100.00"
LIMIT = 0


def set_product(coin):
    global PRODUCT
    s_coin = str(coin).upper()

    ## match syntax isn't available until v3.10:
    # match s_coin:
    #     case "B" | "BTC" | "BTC-USD":
    #         PRODUCT = "BTC-USD"
    #     case "E" | "ETH" | "ETH-USD":
    #         PRODUCT = "ETH-USD"
    #     case "S" | "SOL" | "SOL-USD":
    #         PRODUCT = "SOL-USD"
    #     case _:
    #         if s_coin.find("-") == -1:
    #             PRODUCT = s_coin + "-USD"
    #         else:
    #             PRODUCT = s_coin
    if s_coin == "B" or s_coin =="BTC" or s_coin == "BTC-USD":
        PRODUCT = "BTC-USD"
    elif s_coin == "E" or s_coin == "ETH" or s_coin == "ETH-USD":
        PRODUCT = "ETH-USD"
    elif s_coin == "S" or s_coin == "SOL" or s_coin == "SOL-USD":
        PRODUCT = "SOL-USD"
    elif s_coin.find("-") == -1:
        PRODUCT = s_coin + "-USD"
    else:
        PRODUCT = s_coin

def process_cli_args():
    global ARGS, DEBUG, TEST_MODE, FUNDS, LIMIT
    parser = argparse.ArgumentParser(
        description="Buys digital assets on Coinbase Advanced.",
        epilog="Thanks for using %(prog)s at your own risk! :)")
    use_opt = parser.add_argument_group("configuring purchases")
    use_opt.add_argument("action", help="buy|test - live buy or simulation")
    use_opt.add_argument("-c", "--coin", help="the asset to purchase, such as b|e|s|BTC|ETH|SOL|BTC-USD. Default BTC-USD.", default="BTC-USD")
    use_opt.add_argument("-f", "--funds", help="the amount to spend. Default 100.00.", default="100.00")
    use_opt.add_argument("-l", "--limit", help="0|1|5 - percent limit order discount. Default 0.0 (market order).", type=float, default=0.0)
    #opt_opt = parser.add_argument_group("options")
    parser.add_argument("-d", "--debug", action="store_true", help="toggle verbose logging")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    ARGS = parser.parse_args()
    DEBUG = ARGS.debug
    match str(ARGS.action).lower():
        case "test":
            TEST_MODE = True
            print("TEST MODE ACTIVATED.")
        case "buy":
            TEST_MODE = False
        case _:
            print("Impossible action - quitting.")
            exit(1)
    set_product(ARGS.coin)
    FUNDS = ARGS.funds
    LIMIT = ARGS.limit

# '''
# ### Usage
#       nodejs ./dcaCoinbasePro/dca-client.js (--help|-h)
#       nodejs ./dcaCoinbasePro/dca-client.js --config env key secret passphrase
#       nodejs ./dcaCoinbasePro/dca-client.js --showConfig env key
#       nodejs ./dcaCoinbasePro/dca-client.js (test|prod) [buy] key
#     Arguments:
#       --config     - create encrypted API key.
#         env        - 'test' or 'prod'.
#         key        - API key.
#         secret     - API secret.
#         passphrase - API passphrase.
#       --showConfig - show a configuration.
#         env        - 'test' or 'prod'.
#         key        - encryption key.
#       test         - use sandbox API (default).
#       prod         - use production API.
#       buy          - order a purchase trade.
#       key          - encryption key.

def update_config_file(CONFIG_FILE, section, option, value):
    # Read the INI file.
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    # Update a value.
    old = config.get(section, option)
    print(f"Updating {CONFIG_FILE} option {section}:{option} from '{old}' to '{value}'.")
    config.set(section, option, value)

    # Write changes back to the file.
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def fetch_config_file(CONFIG_FILE):
    # Create a ConfigParser object.
    config = configparser.ConfigParser()

    # Read the INI file.
    config.read(CONFIG_FILE)

    # Set global variables, accessing values via section and option names.
    global API_KEY, API_SECRET, CONFIG
    API_KEY = config.get("API", "API Key").strip('"')
    API_SECRET = config.get("API", "API Secret").strip('"')
    CONFIG = config

    return CONFIG

def gen_uuid():
    random_uuid = uuid.uuid4()
    return random_uuid

def test_coinbase(client):
    accounts = client.get_accounts(limit=250)
    print(dumps(accounts, indent=2))

# @arg client - an opened Coinbase RESTClient connection object.
# @arg str_market - the product to buy, such as "BTC-USD" for BTC.
# @arg str_amount - the amount to spend, such as "100" for $100.
def place_market_buy(client, str_market, str_amount):
    order_uuid = str(gen_uuid())
    order = client.market_order_buy(
        client_order_id=order_uuid,
        product_id=str_market,
        quote_size=str_amount
    )

    order_id = order["order_id"]

    if bool(order["success"]):
        if DEBUG:
            print(order)
        fills = client.get_fills(order_id=order_id)
        print(dumps(fills, indent=2))
    else:
        print(f"Error placing market order #{order_uuid}:")
        print(order)
    return order_id

# @arg client - an opened Coinbase RESTClient connection object.
# @arg str_market - the product to buy, such as "BTC-USD" for BTC.
# @arg str_quantity - how much to buy, such as "0.001" for 100k sats.
# @arg fp_price - the limit price, such as "67000" for $67k.
def place_limit_buy(client, str_market, str_quantity, fp_price):
    order_uuid = str(gen_uuid())
    limit_order = client.limit_order_gtc_buy(
        client_order_id=order_uuid,
        product_id=str_market,
        base_size=str_quantity,
        limit_price=fp_price,
        post_only=True
    )

    limit_order_id = limit_order["order_id"]
    if bool(limit_order["success"]):
        if DEBUG:
            print(limit_order)
    else:
        print(f"Error placing limit order #{order_uuid}:")
        print(limit_order)
    return limit_order_id

def cancel_order(client, order_id):
    client.cancel_orders(order_ids=[order_id])

def main():
    process_cli_args()

    fetch_config_file(CONFIG_FILE)
    if DEBUG:
        print(CONFIG)
        print(API_KEY)
        print(API_SECRET)

    client = RESTClient(api_key=API_KEY, api_secret=API_SECRET, verbose=DEBUG)
    
    # Test Coinbase Advanced.
    if DEBUG:
        test_coinbase(client)
        random_uuid = gen_uuid()
        print(random_uuid)
    
    ## Examples follow:
    ## Market buy $10 of BTC.
    #place_market_buy(client, "BTC-USD", "10")
    ## Limit buy 20k sats at $64k/BTC.
    #place_limit_buy(client, "BTC-USD", "0.0002", "64000")

    product = client.get_product(PRODUCT)
    if DEBUG:
        print(product)
    str_price = str(product["price"])
    asset_price = float(product["price"])
    print(f"Current {PRODUCT} market price is ${str_price}.")
    if LIMIT == 0.0:
        # When no limit order discount is requested, use a market order.
        if TEST_MODE:
            print(f"I would have market bought ${FUNDS} of {PRODUCT}.")
        else:
            place_market_buy(client, PRODUCT, FUNDS)
    else:
        # Otherwise place a limit order at a discounted price.
        #low_price = str(math.floor(asset_price * (100.0-LIMIT)/100.0))
        str_base_increment = str(product["base_increment"])
        fl_base_increment = float(product["base_increment"])
        units_mantissa_len = len(str_base_increment) - str_base_increment.find(".") - 1
        price_mantissa_len = len(str_price) - str_price.find(".") - 1
        low_price = round(asset_price * (100.0-LIMIT)/100.0, price_mantissa_len)
        # quantity = str(round(float(FUNDS) / float(low_price), units_mantissa_len))  # May round over budget
        quantity = str(round(math.floor(float(FUNDS) / float(low_price) / fl_base_increment) * fl_base_increment, units_mantissa_len))
        str_low_price = str(low_price)
        if TEST_MODE:
            print(f"I would have limit ordered {quantity} of {PRODUCT} at {str_low_price} (${round(float(quantity)*low_price, price_mantissa_len)}).")
        else:
            order_id = place_limit_buy(client, PRODUCT, quantity, str_low_price)
            print(f"Limit order {order_id} placed for {quantity} {PRODUCT} @ {str_low_price} (${round(float(quantity)*low_price, price_mantissa_len)}).")
            print("May the odds be ever in your favor.")
            #cancel_order(client, order_id)


main()

