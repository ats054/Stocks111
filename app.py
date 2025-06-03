import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="תחזית זהב, מניות וקריפטו", layout="centered")
st.title("📈 תחזית מבוססת מגמה אמיתית")
st.write("בחר נכס, טווח זמן וסכום השקעה – התחזית תבוסס על שינויי מחירים אמיתיים בזמן האחרון.")

stocks = {
    'נאסד"ק': '^IXIC',
    'S&P 500': '^GSPC',
    'זהב': 'GC=F',
    'ביטקוין': 'BTC-USD',
    'ת"א 35': 'TA35.TA',
    'נפט': 'CL=F'
}

interval_map = {
    '1 דקה': '1m',
    '5 דקות': '5m',
    '10 דקות': '15m',
    '30 דקות': '30m',
    'שעה': '60m'
}

selected_stock = st.selectbox("בחר נכס", list(stocks.keys()))
selected_time = st.selectbox("בחר טווח זמן", list(interval_map.keys()))
amount = st.number_input("סכום השקעה ($)", min_value=1, value=1000)

def calculate_trend(data):
    change = data['Close'].pct_change().dropna()
    avg_change = change[-5:].mean()
    if avg_change > 0.001:
        return "קנייה 🔼", avg_change
    elif avg_change < -0.001:
        return "מכירה 🔽", avg_change
    else:
        return "המתן ⚠️", avg_change

if st.button("קבל תחזית"):
    try:
        interval = interval_map[selected_time]
        ticker = stocks[selected_stock]
        data = yf.download(ticker, period='1d', interval=interval)
        if data.empty or 'Close' not in data:
            raise ValueError("אין נתונים זמינים")

        trend, change = calculate_trend(data)
        current_price = data['Close'].iloc[-1]
        predicted_price = current_price * (1 + change)
        profit = predicted_price * amount / current_price - amount

        st.success(f"תחזית ל-{selected_stock} בטווח {selected_time}: {trend}")
        st.info(f"שינוי מגמה אחרון: {change*100:.2f}%")
        st.info(f'רווח/הפסד צפוי: ${profit:.2f} (סה"כ: ${amount + profit:.2f})')

        st.line_chart(data['Close'])
    except Exception as e:
        st.error(f"שגיאה: {e}")
