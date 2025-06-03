import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import feedparser

# הגדרת עמוד
st.set_page_config(page_title="תחזית חכמה - בינה מלאכותית", layout="centered")
st.title("🔮 תחזית זהב, מניות וקריפטו מבוססת בינה מלאכותית")
st.write("בחר נכס, טווח זמן וסכום השקעה - ותקבל תחזית עם רמת ביטחון וחדשות רלוונטיות.")

# רשימת נכסים
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

# טווחי זמן
intervals = {
    '1 דקה': '1m',
    '5 דקות': '5m',
    '10 דקות': '15m',
    '30 דקות': '30m',
    'שעה': '60m',
    'יום': '1d',
    'שבוע': '1wk'
}

# פונקציה לחישוב רמת ביטחון
def calculate_confidence(data):
    confidence = 0
    total = 3

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

    return round((confidence / total) * 100)

# פונקציה להצגת חדשות
def show_news(query):
    st.subheader("🗞 חדשות עדכניות")
    try:
        query_encoded = query.replace(" ", "+")
        rss_url = f"https://news.google.com/rss/search?q={query_encoded}+stock&hl=en-US&gl=US&ceid=US:en"
        feed = feedparser.parse(rss_url)
        if not feed.entries:
            st.info("לא נמצאו חדשות עדכניות.")
        for entry in feed.entries[:5]:
            st.markdown(f"🔹 [{entry.title}]({entry.link})")
    except Exception as e:
        st.warning(f"שגיאה בטעינת החדשות: {e}")

# ממשק בחירה
selected_stock = st.selectbox("בחר נכס", list(stocks.keys()))
selected_interval_label = st.selectbox("בחר טווח זמן", list(intervals.keys()))
amount = st.number_input("סכום השקעה ($)", min_value=1, value=1000)

# לחצן פעולה
if st.button("קבל תחזית"):
    try:
        symbol = stocks[selected_stock]
        interval = intervals[selected_interval_label]
        data = yf.download(symbol, period='5d', interval=interval)

        if data.empty or 'Close' not in data:
            raise ValueError("אין נתוני סגירה זמינים")

        current_price = data['Close'].iloc[-1]
        confidence = calculate_confidence(data)
        recommendation = "קנייה 🔼" if confidence >= 66 else "להימנע ❌" if confidence < 50 else "מכירה 🔽"
        expected_return = amount * (1 + (confidence - 50) / 100)
        profit = expected_return - amount

        st.success(f"תחזית ל-{selected_stock} בטווח {selected_interval_label}: {recommendation}")
        st.info(f"💰 רווח/הפסד צפוי: ${profit:.2f} (סה\"כ: ${expected_return:.2f})")
        st.warning(f"🔎 רמת ביטחון בתחזית: {confidence}%")

        # חדשות
        show_news(selected_stock)
    except Exception as e:
        st.error(f"אירעה שגיאה: {e}")
