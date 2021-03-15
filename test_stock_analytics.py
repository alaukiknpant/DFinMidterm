from aum_calculator import AumCalculator
import matplotlib.pyplot as plt
import pandas as pd



class Test():

    def __init__(self, prices_dataframe, initial_aum):
        self.df = prices_dataframe
        self.initial_aum = initial_aum
        self.calculator = AumCalculator(df, initial_aum)
        
    def test_returns(self):

        calendar_days = 3

        total_stock_return = self.calculator.get_total_stock_return()

        total_return = self.calculator.get_total_return(total_stock_return)

        annualized_rate_of_return = self.calculator.get_annualized_rate_return(calendar_days)

        final_aum = self.calculator.get_final_aum(total_return)

        average_aum, max_aum = self.calculator.get_avg_and_max_aum()

        avg_daily_return, daily_std = self.calculator.get_avg_daily_return_and_std_portfolio()

        pnl = self.calculator.get_pnl(final_aum)

        avg_daily_return, daily_std = self.calculator.get_avg_daily_return_and_std_portfolio()

        risk_free_rate = 0.01

        sharpe_ratio = self.calculator.get_daily_sharpe_ratio (avg_daily_return, risk_free_rate, daily_std)

        assert(total_stock_return == -0.44743424706555934)
        assert(total_return == -223.7171235327769)
        assert(annualized_rate_of_return == 0.0)
        assert(final_aum == 49776.28287646722)
        assert(average_aum == 49850.855250978144)
        assert(max_aum == 50000)
        assert(avg_daily_return == -0.22371712353277967)
        assert(daily_std == 0.3163837902351541)
        assert(pnl == -223.7171235327769)
        assert(risk_free_rate == 0.01)
        assert(sharpe_ratio == -0.7387139630607119)


    def test_plot(self):
        fig = self.calculator.plot()
        assert(plt.axes() != None)



if __name__ == "__main__":
    data = {"Close":{"2017-01-03":62.1300010681,"2017-01-04":62.1199989319,"2017-01-05":62.0299987793},
            "Adj Close":{"2017-01-03":58.5384178162,"2017-01-04":58.2764968872,"2017-01-05":58.2764968872},
    }

    df = pd.DataFrame.from_dict(data)
    initial_aum = 50000
    tester = Test(df, initial_aum)
    print("Testing...")
    tester.test_returns()
    tester.test_plot()
    print("All tests passed!")
   