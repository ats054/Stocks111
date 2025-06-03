import yfinance as yf
import pandas as pd

tickers = {
    'NASDAQ': '^IXIC',
    'S&P 500': '^GSPC',
    'Gold': 'GC=F',
    'Bitcoin': 'BTC-USD',
    'Ethereum': 'ETH-USD',
    'Nvidia': 'NVDA'
}

results = {}
for name, ticker in tickers.items():
    data = yf.download(ticker, period='2d', interval='5m')
    if 'Close' in data and not data.empty:
        data['SMA5'] = data['Close'].rolling(window=5).mean()
        data['SMA20'] = data['Close'].rolling(window=20).mean()
        if pd.notnull(data['SMA5'].iloc[-1]) and pd.notnull(data['SMA20'].iloc[-1]):
            trend = 'Buy' if data['SMA5'].iloc[-1] > data['SMA20'].iloc[-1] else 'Sell'
            change = (data['Close'].iloc[-1] - data['Close'].iloc[-2]) / data['Close'].iloc[-2]
            results[name] = {
                'trend': trend,
                'last_price': data['Close'].iloc[-1],
                'change_%': round(change * 100, 2)
            }

df = pd.DataFrame(results).T
print(df)
