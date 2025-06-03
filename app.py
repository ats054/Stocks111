import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="תחזית חכמה", layout="centered")
st.title("🔮 תחזית חכמה - זהב, מניות וקריפטו")
st.write("בחר נכס, טווח זמן וסכום השקעה - וקבל תחזית עם מגמה ורמת ביטחון.")

stocks = {
    'נאסד"ק (NASDAQ)': '^IXIC',
    'S&P 500': '^GSPC',
    'זהב (Gold)': 'GC=F',
    'נאסד"ק 100 (NDX)': '^NDX',
    'ת"א 35': 'TA35.TA',
    'Nvidia': 'NVDA',
    'ביטקוין (Bitcoin)': 'BTC-USD',
    "את'ריום (Ethereum)": 'ETH-USD',
    'נפט גולמי': 'CL=F'
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

# חישוב רמת ביטחון משולבת
def calculate_confidence(data):
    score = 0
    total = 3

    data['SMA5'] = data['Close'].rolling(window=5).mean()
    data['SMA20'] = data['Close'].rolling(window=20).mean()
    if data['SMA5'].iloc[-1] > data['SMA20'].iloc[-1]:
        score += 1

    delta = data['Close'].diff()
    gain = delta.clip(lower=0).rolling(window=14).mean()
    loss = -delta.clip(upper=0).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    if rsi.iloc[-1] < 70:
        score += 1

    exp1 = data['Close'].ewm(span=12).mean()
    exp2 = data['Close'].ewm(span=26).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9).mean()
    if macd.iloc[-1] > signal.iloc[-1]:
        score += 1

    return round((score / total) * 100)

# UI
selected_stock = st.selectbox("בחר נכס", list(stocks.keys()))
selected_interval = st.selectbox("בחר טווח זמן", list(intervals.keys()))
amount = st.number_input("סכום השקעה ($)", min_value=1, value=1000)

if st.button("קבל תחזית"):
    try:
        symbol = stocks[selected_stock]
        interval = intervals[selected_interval]
        data = yf.download(symbol, period='5d', interval=interval)

        if data.empty or 'Close' not in data:
            raise ValueError("אין נתוני סגירה זמינים")

        current_price = data['Close'].iloc[-1]
        confidence = calculate_confidence(data)

        recommendation = "קנייה 🔼" if confidence >= 66 else "להימנע ❌" if confidence < 50 else "מכירה 🔽"
        predicted_price = current_price * (1.01 if recommendation == "קנייה 🔼" else 0.99)
        profit = predicted_price * amount / current_price - amount

        st.subheader(f"📊 תחזית ל־{selected_stock} בטווח {selected_interval}")
        st.write(f"📈 מגמה: **{recommendation}**")
        st.write(f"💰 רווח/הפסד צפוי: **${profit:.2f}**")
        st.write(f"🔐 רמת ביטחון: **{confidence}%**")

    except Exception as e:
        st.error(f"אירעה שגיאה: {str(e)}")
