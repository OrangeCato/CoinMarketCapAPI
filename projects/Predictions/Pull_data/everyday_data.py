import json
import requests
import sqlite3
from datetime import datetime
import os

def fetch_and_insert_crypto_data(api_key, local_currency, start, db_path):
    local_symbol = '$'

    headers = {'X-CMC_PRO_API_KEY': api_key}
    base_url = 'https://pro-api.coinmarketcap.com'

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for i in range(10):
        listings_url = base_url + '/v1/cryptocurrency/listings/latest?convert=' + local_currency + '&start=' + str(start)
        request = requests.get(listings_url, headers=headers)
        results = request.json()
        data = results['data']

        current_date = datetime.now().date()

        for currency in data:
            name = currency['name']
            symbol = currency['symbol']

            quote = currency['quote'][local_currency]
            market_cap = quote['market_cap']
            hour_change = quote['percent_change_1h']
            day_change = quote['percent_change_24h']
            week_change = quote['percent_change_7d']
            price = quote['price']
            volume = quote['volume_24h']

            insert_query = 'INSERT OR IGNORE INTO daily_crypto_data (symbol, "name", market_cap, price, volume_24h, hour_change, day_change, week_change, pull_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
            values = (symbol, name, market_cap, price, volume, hour_change, day_change, week_change, current_date)

            cursor.execute(insert_query, values)
            conn.commit()

        start += 100

    conn.close()

# Example usage in your main script:
if __name__ == "__main__":
    # set env variable e.g. export coinmarketcap_api_key=YOUR_API_KEY
    api_key = os.environ.get('coinmarketcap_api_key')
    local_currency = 'USD'
    start = 1
    db_path = '/Users/alessandrazamora/Desktop/MLrsc/CoinMarketCap/projects/HistoricalData/Data_updated_24h.db'

    fetch_and_insert_crypto_data(api_key, local_currency, start, db_path)