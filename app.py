import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="תחזית מניות וזהב", layout="centered")
st.title("📈 תחזית חכמה - מניות, זהב וקריפטו")

stocks = {
    'נאסד"ק': '^IXIC',
    'S&P 500': '^GSPC',
    'זהב': 'GC=F',
    'ביטקוין': 'BTC-USD',
    'אתריום': 'ETH-USD'
}

intervals = {
    '5 דקות': '5m',
    '30 דקות': '30m',
    'יום': '1d'
}

selected_stock = st.selectbox("בחר נכס", list(stocks.keys()))
selected_time = st.selectbox("בחר טווח זמן", list(intervals.keys()))
amount = st.number_input("סכום השקעה ($)", min_value=1, value=1000)

def analyze_trend(data):
    data['SMA5'] = data['Close'].rolling(5).mean()
    data['SMA20'] = data['Close'].rolling(20).mean()
    sma5 = float(data['SMA5'].iloc[-1]) if pd.notna(data['SMA5'].iloc[-1]) else None
    sma20 = float(data['SMA20'].iloc[-1]) if pd.notna(data['SMA20'].iloc[-1]) else None

    if sma5 is None or sma20 is None:
        return "לא מספיק נתונים", 1.00
    elif sma5 > sma20:
        return "קנייה 🔼", 1.02
    else:
        return "מכירה 🔽", 0.98

if st.button("קבל תחזית"):
    try:
        ticker = stocks[selected_stock]
        interval = intervals[selected_time]
        data = yf.download(ticker, period='1d', interval=interval)
        if data.empty or 'Close' not in data:
            raise ValueError("אין נתונים זמינים")

        close_price = data['Close'].dropna().iloc[-1]
        current_price = float(close_price)
        trend, multiplier = analyze_trend(data)
        predicted_price = current_price * multiplier
        profit = predicted_price - current_price
        profit_dollars = profit * (amount / current_price)

        st.success(f"תחזית ל-{selected_stock}: {trend}")
        st.info(f"רווח/הפסד צפוי: ${profit_dollars:.2f} (סה\"כ: ${(amount + profit_dollars):.2f})")
    except Exception as e:
        st.error(f"שגיאה: {str(e)}")
