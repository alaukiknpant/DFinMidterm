## Data Science for Quantative finance Midterm

Name: Alaukik Pant

## Commands to Run for analytics

```
python3 get_prices.py --ticker MSFT --b 20201103 --e 20210301 --initial_aum 1 --plot
python3 get_prices.py --ticker msft --b 20100101 --initial_aum 1000000
python3 get_prices.py --ticker SPY --b 20210101 --e 20210301 --initial_aum 1000000
python3 get_prices.py --ticker GOOG --b 20301010 --initial_aum 10000
python3 get_prices.py --ticker GOOG --b 20101010 --initial_aum 10000
python3 get_prices.py --ticker LSEG.L --b 19000101 --e 20201231 --initial_aum 10000 --plot
python3 get_prices.py --ticker yalenus --b 19000101 --e 20201231 --initial_aum 10000 --plot
```


## Command to Run for tests

```
python3 test_stock_analytics.py
```


## Notes

- Yahoo finance API fetches stock price of day after the begin date and the day before the end date. I was not sure if the aim of the assignment was to manipulate dates. Hence, I stuck with Yahoo finance API guidelines.

- My terminal could not recognize the `--b` or `--e` that was given. But when I run the afformentioned commands, the scripts run smoothly.

- I've expressed the average daily return and daily Standard deviation of the return of the portfolio as percentages. I was not clear weather it was meant to be expressed as actual amounts. The way to express actual amounts have been commented in the code.