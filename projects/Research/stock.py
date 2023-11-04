import requests
import os

def get_current_markets():
    # set env variable e.g. export coinmarketcap_api_key=YOUR_API_KEY
    api_key = os.environ.get('alpha_key')
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics=financial_markets&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    print(data)
    
get_current_markets()