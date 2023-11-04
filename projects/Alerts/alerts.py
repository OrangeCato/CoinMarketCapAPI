import os
import csv
import sys
import json
import time
import requests
from datetime import datetime

local_currency = 'USD'
local_symbol = '$'
# set env variable e.g. export coinmarketcap_api_key=YOUR_API_KEY
api_key = os.environ.get('coinmarketcap_api_key')
headers = {'X-CMC_PRO_API_KEY': api_key}

base_url = 'https://pro-api.coinmarketcap.com'

print()
print("ALERTS TRACKING...")
print()

already_hit_symbols = []

while True:
    with open("MyAlerts.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            if "\ufeff" in line[0]:
                line[0] = line[0][1:].upper()
            else:
                line[0] = line[0].upper()
            symbol = line[0]
            amount = line[1]
            
            ticker_url = base_url + '/v1/cryptocurrency/quotes/latest?convert=' + local_currency + '&symbol=' + symbol
            
            request = requests.get(ticker_url, headers=headers)
            results = request.json()
            currency = results['data'][symbol]
            name = currency['name']
            price = currency['quote'][local_currency]['price']
            
            if float(price) >= float(amount) and symbol not in already_hit_symbols:
                os.system('say ALERT ALERT ALERT')
                os.system('say ' + name + ' hit ' + amount)
                sys.stdout.flush()
                
                now = datetime.now()
                current_time = now.strftime('%H:%M%p')
                print(name + ' hit ' + amount + ' at ' + current_time + '!')
                already_hit_symbols.append(symbol)
                
    print('...')
    time.sleep(10)