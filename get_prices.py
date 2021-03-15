import argparse
import numpy as np
import os
import warnings
import matplotlib.pyplot as plt
from aum_calculator import AumCalculator
import yfinance as yf
from datetime import datetime
import pandas as pd
from yahoofinancials import YahooFinancials
from pandas_datareader import data as pdr
import requests

## Name - Alaukik Nath Pant


def main():
    """
    
    Main function with all the helper functions

    """

    def get_symbol(symbol):
        url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)

        result = requests.get(url).json()

        for x in result['ResultSet']['Result']:
            if x['symbol'] == symbol:
                return x['name']


    def convert_date(date):
        """
        Function that converts date to the required format

        Returns: String representing date

        """
        return datetime.strptime(str(date),'%Y%m%d').strftime('%Y-%m-%d')

    def days_between(d1, d2):
        d1 = datetime.strptime(d1, "%Y-%m-%d")
        d2 = datetime.strptime(d2, "%Y-%m-%d")
        return (d2 - d1).days


    parser = argparse.ArgumentParser(description='Process arguments')

    def enable_parsing(parser):
        """
        Function that adds the arguments to our parser

        Returns: None

        """
        parser.add_argument("--ticker", help="Stock ticker (e.g., MSFT) as <xxx>",
                            required=True)
        parser.add_argument("--b", help="Begin Date as <YYYYMMDD>",
                            required=True)
        parser.add_argument("--e", help="End Date as <YYYYMMDD>")

        parser.add_argument("--initial_aum", help="Initial asset under management",
                            type=int, required=True)

        parser.add_argument('--plot', help="To plot",
                            action='store_true')
        return parser


    parser = enable_parsing(parser)
    args = parser.parse_args()

    TICKER = args.ticker.upper()
    BEGIN_DATE = convert_date(args.b)
    END_DATE= convert_date(args.e) if args.e != None else datetime.today().strftime('%Y-%m-%d')
    initial_aum = args.initial_aum
    TO_PLOT = args.plot

    if (days_between(END_DATE, BEGIN_DATE)) > 0:
        print("End Date should be after begin date... Please try again")
        quit()

    try:
        yf.pdr_override() 
        df = pdr.get_data_yahoo(TICKER, 
                                BEGIN_DATE,
                                    END_DATE)
        
        company = get_symbol(TICKER)
    except:
        print("Could not find ticker... Please try again")
        quit()

    calculator = AumCalculator(df, initial_aum)

    start_date, end_date = calculator.get_dates(df)

    calendar_days = calculator.get_calender_days(start_date, end_date)

    total_stock_return = calculator.get_total_stock_return()

    total_return = calculator.get_total_return(total_stock_return)

    annualized_rate_of_return = calculator.get_annualized_rate_return(calendar_days)

    final_aum = calculator.get_final_aum(total_return)

    average_aum, max_aum = calculator.get_avg_and_max_aum()

    avg_daily_return, daily_std = calculator.get_avg_daily_return_and_std_portfolio()

    pnl = calculator.get_pnl(final_aum)

    avg_daily_return, daily_std = calculator.get_avg_daily_return_and_std_portfolio()

    risk_free_rate = 0.01

    sharpe_ratio = calculator.get_daily_sharpe_ratio (avg_daily_return, risk_free_rate, daily_std)

    print("\n Company: " + company + "\n\n")
    print("1. Start date is: " + start_date + "\n\n")
    print("2. End date is: " + end_date + "\n\n")
    print("3. Number of Calendar Days is: " + str(calendar_days) + "\n\n")
    print("4. Total Stock return(adjusted for dividends) is: " + str(total_stock_return) + "%\n\n")
    print("5. Total return (of the AUM invested) is: " + str(total_return) + "\n\n")
    print("6. Annualized rate of return (of the AUM invested): " + str(annualized_rate_of_return) + "%\n\n")
    print("7. Initial AUM is: " + str(initial_aum) + "\n\n")
    print("8. Final AUM is: " + str(final_aum) + "\n\n")
    print("9. Average AUM is: " + str(average_aum) + "\n\n")
    print("10. Maximum AUM: " + str(max_aum) + "\n\n")
    print("11. PnL (of the AUM invested) is: " + str(pnl) + "\n\n")
    print("12. Average daily return of the portfolio (i.e., of the AUM invested) is: " + str(avg_daily_return) + "%\n\n")
    print("13. Daily Standard deviation of the return of the portfolio is: " + str(daily_std) + "%\n\n")
    print("14. Daily Sharpe Ratio of the portfolio (assume a daily risk-free rate of 0.01%): " + str(sharpe_ratio) + "\n\n")

    if TO_PLOT:
        calculator.plot()
        plt.show()

if __name__ == "__main__":
    try:
        main()
    except:
        print("Please provide new command. Did not accept current command.")




    