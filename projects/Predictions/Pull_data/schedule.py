import os
import schedule
import time

def run_pull_data():
    os.system('python3 /Users/alessandrazamora/Desktop/MLrsc/CoinMarketCap/Projects/Predictions/Pull_data/everyday_data.py')
    
schedule.every(24).hours.dp(run_pull_data)

while True:
    schedule.run_pending()
    time.sleep(1)