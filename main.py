from Projects.Top100.top100 import top_100
from Projects.Research.research import calculate_and_print_global_metrics
from Projects.Portfolio.portfolio import calculate_and_print_portfolio
from colorama import Fore, Back, Style
# import latest, correlation, predictive and sentiment

def main():
    print(Fore.CYAN + "Welcome to EasyStonks. Please select an option:" + Style.RESET_ALL)
    print(Fore.GREEN + "1. Ranking - top 100")
    print(Fore.YELLOW + "2. Global Market Metrics")
    print(Fore.MAGENTA + "3. Your Portfolio")
    print(Fore.BLUE + "4. Your Alerts")
    print(Fore.RED + "5. View Latest Cryptocurrency Data (Last 24 Hours)")
    print(Fore.LIGHTMAGENTA_EX + "6. Assess Risk Management with Correlation Analysis")
    print(Fore.LIGHTCYAN_EX + "7. Evaluate Investments with Predictive Analysis")
    print(Fore.LIGHTGREEN_EX + "8. Perform Sentiment Analysis on Twitter (Enter a keyword, e.g., BTC)" + Style.RESET_ALL)

    choice = input(Fore.CYAN + "Enter the number of your choice: " + Style.RESET_ALL)
    
    if choice == "1":
        top_100()
    elif choice == "2":
        calculate_and_print_global_metrics()
    elif choice == "3":
        calculate_and_print_portfolio()
    elif choice == "4":
        print("Here you should call the Alerts script, but modify it so it allows user to add - delete - modify alerts based on the cryptocurrencies of interest")
    elif choice == "5":
        print("View stats of latest cryptocurrency data (top 1000 - 24h)")
    
    
if __name__ == "__main__":
    main()
