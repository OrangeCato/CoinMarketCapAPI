import requests

def get_current_markets():
    api_key = 'YOUR_API_KEY'
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics=financial_markets&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    print(data)
    
get_current_markets()