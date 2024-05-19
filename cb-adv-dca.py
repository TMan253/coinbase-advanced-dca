import configparser
from json import dumps
from coinbase.rest import RESTClient
import uuid
import math

CONFIG_FILE="config.ini"
CONFIG=""
API_KEY=""
API_SECRET=""


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

    fills = client.get_fills(order_id=order_id)
    print(dumps(fills, indent=2))
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
        limit_price=fp_price
    )

    limit_order_id = limit_order["order_id"]
    return limit_order_id

def cancel_order(client, order_id):
    client.cancel_orders(order_ids=[order_id])

def main():
    fetch_config_file(CONFIG_FILE)
    print(CONFIG)
    print(CONFIG.get("DEFAULT", "asdf"))
    #print(API_KEY)
    #print(API_SECRET)

    #test Coinbase Advanced
    client = RESTClient(api_key=API_KEY, api_secret=API_SECRET)
    #test_coinbase(client)
    #random_uuid = gen_uuid()
    #print(random_uuid)
    ## Market buy $10 of BTC.
    #place_market_buy(client, "BTC-USD", "10")
    ## Limit buy 20k sats at $64k/BTC.
    #place_limit_buy(client, "BTC-USD", "0.0002", "64000")
    #cancel_order(client, order_id)

    product = client.get_product("BTC-USD")
    btc_usd_price = float(product["price"])
    low_btc_usd_price = str(math.floor(btc_usd_price * 0.95))
    print(low_btc_usd_price)
    order_id = place_limit_buy(client, "BTC-USD", "0.0002", low_btc_usd_price)
    cancel_order(client, order_id)


main()

