import pandas.io.data as web

instruments = ['AAPL', 'IBM', 'AMZN', 'MSFT', 'GOOG']

start = '20%02d-01-03'
end = '20%02d-12-30'


for i in range(9):
    start_balance = 100.0
    final_balance = 100.0

    p1 = start % (i + 6)
    p2 = end   % (i + 6)
    data = web.DataReader(name='IBM', data_source='yahoo', start=p1, end=p2)
    start_price = data["Close"][0]

    end_price = data["Close"].tail(1)[0]

    buy_hold = 0

    if (start_price < end_price):
        buy_hold = ((end_price - start_price) / start_price) * 100
    else:
        buy_hold =  -(((start_price - end_price) / end_price) * 100)

    print "Year %s;  B&H %f" % (p1.split('-')[0], buy_hold)
