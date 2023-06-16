import requests
import json

local_currency = 'USD'
local_symbol = '$'
api_key = '6ca83e50-96ec-453c-bb9f-40f2d321ce2d'
headers = {'X-CMC_PRO_API_KEY': api_key}

base_url = 'https://pro-api.coinmarketcap.com'

global_url = base_url + '/v1/cryptocurrency/listings/latest?convert=' + local_currency

request = requests.get(global_url, headers=headers)
results = request.json()

data = results["data"]

for currency in data:
    name = currency["name"]
    symbol = currency["symbol"]

    price = currency["quote"][local_currency]["price"]
    percent_change_24h = currency["quote"][local_currency]['percent_change_24h']
    market_cap = currency["quote"][local_currency]["market_cap"]

    price = round(price, 2)
    percent_change_24h = round(percent_change_24h, 2)
    market_cap = round(market_cap, 2)

    price_string = local_symbol + '{:,}'.format(price)
    percent_change_24h_string = local_symbol + '{:,}'.format(percent_change_24h)
    market_cap_string = local_symbol + '{:,}'.format(market_cap)

    print(name + ' (' + symbol + ')')
    print('Price: ' + price_string)
    print('24h change: ' + percent_change_24h_string)
    print('Market cap: ' + market_cap_string)
    print()
