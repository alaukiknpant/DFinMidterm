import numpy as np
import matplotlib.pyplot as plt
import statistics
from datetime import datetime
import pandas as pd
from yahoofinancials import YahooFinancials


class AumCalculator():

    def __init__(self, prices_dataframe, initial_aum):
        self.prices_dataframe = prices_dataframe
        self.initial_aum = initial_aum
       

    def get_dates(self, prices_dataframe):
        """
        Question 1 and 2

        Finds the start date and end date adjusted for holidays
        Args:
            prices_dataframe: dataframe with information of the stock

        Returns: Tuple of start date and end date

        """
        start_date = prices_dataframe.iloc[0].name.strftime("%Y-%m-%d")
        end_date = prices_dataframe.iloc[len(prices_dataframe) -1].name.strftime("%Y-%m-%d")
        return (start_date, end_date)

        

    def get_calender_days(self, d1, d2):
        """
        Question 3

        calculate prediction given new x value
        Args:
            d1: start date
            d2: end date

        Returns: calendar days between start date and end date

        """
        d1 = datetime.strptime(d1, "%Y-%m-%d")
        d2 = datetime.strptime(d2, "%Y-%m-%d")
        return (d2 - d1).days

    def get_total_stock_return(self):
        """
        Question 4

        Args:
            prices_dataframe: dataframe with information of the stock
            

        Returns: total stock return (adjusted for dividends) as a percentage

        """
        begin_adj_price = self.prices_dataframe.iloc[0]['Adj Close']
        end_adj_price = self.prices_dataframe.iloc[len(self.prices_dataframe) - 1]['Adj Close']
        stock_return_adj_percent = ((end_adj_price - begin_adj_price)/begin_adj_price) * 100
        return stock_return_adj_percent 
    
    def get_total_return(self, stock_return_adj_percent):
        """
        Question 5

        Args:
            stock_return_adj_percent : total stock return (adjusted for dividends) as a percentage

        Returns: total return (of the AUM invested)

        """
        total_return = self.initial_aum * (1 + stock_return_adj_percent/100) - self.initial_aum
        return total_return 


    def get_annualized_rate_return (self, calendar_days):
        """
        Question 6

        Args:
            prices_dataframe : dataframe with information of the stock
            calendar_days: calendar days between start date and end date

        Returns: annualized rate of return (of the AUM invested) as a percentage

        """
        cagr = ((((self.prices_dataframe['Adj Close'][-1]) / self.prices_dataframe['Adj Close'][1])) ** (365.0/calendar_days)) - 1
        return cagr * 100


    def get_final_aum (self, total_return):
        """
        Question 8

        Args:
            total_return: total return (of the AUM invested)

        Returns: final aum

        """
        final_aum = self.initial_aum + total_return 
        return final_aum

    
    def _get_stock_price_list(self):
        """

        Returns: List of stock prices for all given dates
        """
        df2 = self.prices_dataframe[['Adj Close']]
        stock_price_list = list(df2['Adj Close'])
        return stock_price_list

    def get_avg_and_max_aum (self):
        """
        Question 9 and 10

        Returns: Tuple of average aum and max aum

        """
        
        stock_price_list = self._get_stock_price_list()
        inital_price = stock_price_list[0]
        aum_list = [self.initial_aum]
        for i in range(1, len(stock_price_list)):
            change = ((stock_price_list[i] - stock_price_list[i-1]) / inital_price) 
            aum_list.append((1 + change) * aum_list[i-1])
        average_aum = sum(aum_list)/len(aum_list)
        max_aum = max(aum_list)
        return (average_aum, max_aum)

    
    def get_pnl (self, final_aum):
        """
        Question 11

        Args:
            final_aum : final aum after return
          

        Returns: PnL (of the AUM invested)

        """
        PnL = final_aum - self.initial_aum 
        return PnL

    def get_avg_daily_return_and_std_portfolio (self):
        """
        Question 12 and 13

        Returns: Tuple containing average daily return of the AUM and Daily Standard deviation of the return 

        """
        
        stock_price_list = self._get_stock_price_list()
        aum_list = [self.initial_aum]
        # return_list = []
        change_list = []
        for i in range(1, len(stock_price_list)):
            change = ((stock_price_list[i] - stock_price_list[i-1]) / stock_price_list[i-1]) * 100 
            change_list.append(change)
            
            # To calculate ammount
            # aum_list.append((1 + change) * aum_list[i-1])
            # return_list.append((1 + change) * aum_list[i-1] - aum_list[i-1])
        # avg_daily_return = sum(return_list)/len(return_list)
        # daily_std = statistics.stdev(return_list)
        avg_daily_return = sum(change_list)/len(change_list)
        daily_std = statistics.stdev(change_list)
        return (avg_daily_return, daily_std)
    
    def get_daily_sharpe_ratio (self, average_daily_return, risk_free_rate, daily_std):
        """
        Question 14

        Args:
            average_daily_return : Average daily return of the portfolio (i.e., of the AUM invested)
            risk_free_rate :  daily risk-free 
            daily_std : Daily Standard deviation of the return of the portfolio

        Returns: Daily Sharpe Ratio of the portfolio 

        """
        sharpe_ratio = (average_daily_return - risk_free_rate)/daily_std
        return sharpe_ratio


    def _get_daily_aum (self):
        """
        Plotting helper function

        Returns: List of daily AUMs

        """
        stock_price_list = self._get_stock_price_list()
        aum_list = [self.initial_aum]
        return_list = []
        for i in range(1, len(stock_price_list)):
            change = ((stock_price_list[i] - stock_price_list[i-1]) / stock_price_list[i-1]) 
            aum_list.append((1 + change) * aum_list[i-1])
        return aum_list

    def plot(self):
        """
        Plots the daily AUM thru time
        
        Returns: None

        """

        x_axis = self.prices_dataframe.index.values
        
        y_axis = self._get_daily_aum()
        fig, ax = plt.subplots(figsize=(10, 10))

        # Add x-axis and y-axis
        ax.scatter(x_axis,
                y_axis,
                color='purple')

        # Set title and labels for axes
        ax.set(xlabel="Date",
            ylabel="AUM in given currency",
            title="Daily AUM of the given Ticker")

        
