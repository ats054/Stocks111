import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="תחזית זהב, מניות וקריפטו", layout="centered")
st.title("🔮 תחזית חכמה - זהב, מניות וקריפטו")
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
    'נפט גולמי': 'CL=F'
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

def calculate_confidence(sma5, sma20):
    # יחס הפער בין הממוצעים כמדד לביטחון
    gap = abs(sma5 - sma20)
    avg = (sma5 + sma20) / 2
    confidence = min(100, max(0, (gap / avg) * 100))
    return round(confidence, 2)

if st.button("קבל תחזית"):
    try:
        ticker = stocks[selected_stock]
        interval = intervals[selected_time]
        data = yf.download(ticker, period='1d', interval=interval)
        
        if data.empty or 'Close' not in data:
            raise ValueError("אין נתוני סגירה זמינים")
        
        data['SMA5'] = data['Close'].rolling(window=5).mean()
        data['SMA20'] = data['Close'].rolling(window=20).mean()
        
        if pd.isna(data['SMA5'].iloc[-1]) or pd.isna(data['SMA20'].iloc[-1]):
            raise ValueError("אין מספיק נתונים לחישוב מגמה")

        sma5 = data['SMA5'].iloc[-1]
        sma20 = data['SMA20'].iloc[-1]
        trend = "קנייה 🔼" if sma5 > sma20 else "מכירה 🔽"
        confidence = calculate_confidence(sma5, sma20)

        current_price = data['Close'].iloc[-1]
        predicted_price = current_price * (1 + 0.01 if trend == "קנייה 🔼" else 1 - 0.01)
        profit = predicted_price * amount / current_price - amount

        st.success(f"בטווח {selected_time}: {trend} תחזית ל-{selected_stock}")
        st.info(f'רווח/הפסד צפוי: ${round(profit, 2)} (סה"כ: ${round(amount + profit, 2)})')
        st.warning(f"🎯 רמת ביטחון בתחזית: {confidence}%")

    except Exception as e:
        st.error(f"אירעה שגיאה בחיזוי הנתונים: {str(e)}")
