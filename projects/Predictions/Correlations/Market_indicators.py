import requests
import os

def fetch_market_indicators(api_key, time_start, time_end, count, interval, convert):
    headers = {'X-CMC_PRO_API_KEY': api_key}
    base_url = 'https://pro-api.coinmarketcap.com'
    endpoint = '/v1/global-metrics/quotes/historical'
    
    params = {
        'time_start': time_start,
        'time_end': time_end,
        'count': count,
        'interval': interval,
        'convert': convert,
        'aux': 'btc_dominance, altcoin_market_cap, total_volume_24h'
    }
    
    response = requests.get(base_url + endpoint, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        #print(data)
        # Print the first few data points
        for i in range(min(count, len(data['data']))):
            print(data['data'][i])
    else:
        print('Failed to fetch historical data. Status code:', response.status_code)
    # access latest or historical: /v1/global-metrics/quotes/latest or /historical
    # btc dominance, altcoin season index, crypto market cap, blockchain metrics?, trading  volumes.
    # I NEED TO UPGRADE MY API ACCOUNT TO PULL HISTORICAL DATA
def main():
    # set env variable e.g. export coinmarketcap_api_key=YOUR_API_KEY
    api_key = os.environ.get('coinmarketcap_api_key')
    time_start = ''
    time_end = ''
    count = 10
    interval = 'daily'
    convert = 'USD'

    fetch_market_indicators(api_key, time_start, time_end, count, interval, convert)
    
if __name__ == '__main__':
    main()

