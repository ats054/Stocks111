import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="תחזית בינה מלאכותית - זהב, מניות וקריפטו", layout="centered")
st.title("🤖 תחזית חכמה - זהב, מניות וקריפטו")
st.write("בחר נכס, טווח זמן וסכום השקעה - וקבל תחזית, גרף, רווח צפוי ורמת ביטחון.")

stocks = {
    'נאסד"ק (NASDAQ)': '^IXIC',
    'S&P 500': '^GSPC',
    'זהב (Gold)': 'GC=F',
    'נאסד"ק 100 (NDX)': '^NDX',
    'ת"א 35': 'TA35.TA',
    'Nvidia': 'NVDA',
    'ביטקוין (Bitcoin)': 'BTC-USD',
    "את'ריום (Ethereum)": 'ETH-USD'
}

intervals = {
    '1 דקה': '1m',
    '5 דקות': '5m',
    '10 דקות': '15m',
    '30 דקות': '30m',
    'שעה': '60m',
    'יום': '1d',
    'שבוע': '1wk'
}

def calculate_confidence(data):
    confidence = 0
    total_indicators = 3

    data['SMA5'] = data['Close'].rolling(window=5).mean()
    data['SMA20'] = data['Close'].rolling(window=20).mean()
    if data['SMA5'].iloc[-1] > data['SMA20'].iloc[-1]:
        confidence += 1

    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
    RS = gain / loss
    RSI = 100 - (100 / (1 + RS))
    if RSI.iloc[-1] < 70:
        confidence += 1

    exp1 = data['Close'].ewm(span=12, adjust=False).mean()
    exp2 = data['Close'].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    if macd.iloc[-1] > signal.iloc[-1]:
        confidence += 1

    return round((confidence / total_indicators) * 100)

selected_stock = st.selectbox("בחר נכס", list(stocks.keys()))
selected_interval_label = st.selectbox("בחר טווח זמן", list(intervals.keys()))
amount = st.number_input("סכום השקעה ($)", min_value=1, value=1000)

if st.button("קבל תחזית"):
    try:
        symbol = stocks[selected_stock]
        interval = intervals[selected_interval_label]
        data = yf.download(symbol, period='5d', interval=interval)

        if data.empty:
            raise ValueError("אין נתוני סגירה זמינים")

        current_price = data['Close'].iloc[-1]
        confidence = calculate_confidence(data)
        recommendation = "קנייה 🔼" if confidence >= 66 else "להימנע ❌" if confidence < 50 else "מכירה 🔽"
        expected_return = amount * (1 + (confidence - 50)/100)
        profit = expected_return - amount

        st.success(f"תחזית ל-{selected_stock} בטווח {selected_interval_label}: {recommendation}")
        st.info(f"סכום השקעה: ${amount} | רווח/הפסד צפוי: ${profit:.2f}")
        st.warning(f"רמת ביטחון בתחזית: {confidence}%")
        st.line_chart(data['Close'])

    except Exception as e:
        st.error(f"אירעה שגיאה: {e}")
