import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="תחזית זהב, מניות וקריפטו", layout="centered")
st.title("🔮 תחזית חכמה - זהב, מניות, קריפטו ו־Plus500")
st.write("בחר נכס, טווח זמן וסכום השקעה - וקבל תחזית עם חיווי מיידי.")

stocks = {
    'נאסד"ק (NASDAQ)': '^IXIC',
    'S&P 500': '^GSPC',
    'זהב (Gold)': 'GC=F',
    'נאסד"ק 100 (NDX)': '^NDX',
    'ת"א 35': 'TA35.TA',
    'Nvidia': 'NVDA',
    'ביטקוין (Bitcoin)': 'BTC-USD',
    "את'ריום (Ethereum)": 'ETH-USD',
    'מדד US Tech 100': '^NDX'
}

intervals = {
    '1 דקה': '1m',
    '5 דקות': '5m',
    '10 דקות': '10m',
    '30 דקות': '30m',
    'שעה': '60m',
    'יום': '1d',
    'שבוע': '1wk'
}

selected_stock = st.selectbox("בחר נכס", list(stocks.keys()))
selected_time = st.selectbox("בחר טווח זמן", list(intervals.keys()))
amount = st.number_input("סכום השקעה ($)", min_value=1, step=1, value=1000)

def get_forecast(data):
    data['SMA5'] = data['Close'].rolling(window=5).mean()
    data['SMA20'] = data['Close'].rolling(window=20).mean()
    last = len(data) - 1

    if pd.isna(data['SMA5'].iloc[last]) or pd.isna(data['SMA20'].iloc[last]):
        return "לא בטוח", "❓", 0.5

    if data['SMA5'].iloc[last] > data['SMA20'].iloc[last]:
        confidence = min(abs(data['SMA5'].iloc[last] - data['SMA20'].iloc[last]) / data['SMA20'].iloc[last], 0.25)
        return "קנייה", "🔼", round(0.7 + confidence, 2)
    else:
        confidence = min(abs(data['SMA20'].iloc[last] - data['SMA5'].iloc[last]) / data['SMA5'].iloc[last], 0.25)
        return "מכירה", "🔽", round(0.7 + confidence, 2)

if st.button("קבל תחזית"):
    try:
        ticker = stocks[selected_stock]
        interval = intervals[selected_time]
        data = yf.download(ticker, period='1d', interval=interval)

        if data.empty or 'Close' not in data:
            raise ValueError("אין נתוני סגירה זמינים")

        direction, icon, confidence = get_forecast(data)
        latest_price = data['Close'].iloc[-1]
        predicted_price = latest_price * (1.01 if direction == "קנייה" else 0.99)
        profit = predicted_price * amount / latest_price - amount

        st.success(f"בטווח {selected_time}: {direction} {icon} תחזית ל־{selected_stock}")
        st.info(f'רווח/הפסד צפוי: ${profit:.2f} (סה"כ: ${amount + profit:.2f})')
        st.warning(f'רמת ביטחון בתחזית: {confidence * 100:.1f}%')

        st.line_chart(data['Close'])

    except Exception as e:
        st.error(f"אירעה שגיאה בחיזוי הנתונים: {str(e)}")
