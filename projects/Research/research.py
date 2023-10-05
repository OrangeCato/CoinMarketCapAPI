from email import header
from email.mime import base
import math
import json
import locale
from pickletools import markobject
import requests
from prettytable import PrettyTable

local_currency = 'USD'
local_symbol = '$'

api_key = '6ca83e50-96ec-453c-bb9f-40f2d321ce2d'
headers = {'X-CMC_PRO_API_KEY': api_key}

base_url = 'https://pro-api.coinmarketcap.com'

global_url = base_url + '/v1/global-metrics/quotes/latest?convert=' + local_currency

request = requests.get(global_url, headers=headers)
results = request.json()

data = results["data"]

total_market_cap = int(data["quote"][local_currency]["total_market_cap"])
total_market_cap_string = '{:,}'.format(total_market_cap)

table = PrettyTable(['Name', 'Ticker', '(%) Total Global Cap', 'Price', '10T (Gold)', '48.9T (Narrow Money)',  '109T (Stock Markets)'])

listings_url = base_url + '/v1/cryptocurrency/listings/latest?convert=' + local_currency

request = requests.get(listings_url, headers=headers)
results = request.json()
data = results['data']

for currency in data:
    name = currency['name']
    ticker = currency['symbol']
    
    market_cap = currency['quote'][local_currency]['market_cap']
    
    percentage_of_global_cap = float(market_cap) / float(total_market_cap)
    
    price = currency['quote'][local_currency]['price']
    
    available_supply = currency['total_supply']
    
    gold_price = 1000000000000 * percentage_of_global_cap / available_supply
    
    narrow_money_price = 48900000000000 * percentage_of_global_cap / available_supply
    
    stock_market_price = 109000000000000 * percentage_of_global_cap / available_supply
    
    percentage_of_global_cap_string = str(round(percentage_of_global_cap*100, 2)) + '%'
    price_string = local_symbol + '{:,}'.format(round(price, 2))
    gold_price_string = local_symbol + '{:,}'.format(round(gold_price, 2))
    narrow_money_string = local_symbol + '{:,}'.format(round(narrow_money_price, 2))
    stock_markets_string = local_symbol + '{:,}'.format(round(stock_market_price, 2))
    
    table.add_row([name, ticker, percentage_of_global_cap_string, price_string, gold_price_string, narrow_money_string, stock_markets_string])
    
print()
print(table)
print()
