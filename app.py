
import streamlit as st
import yfinance as yf
import pandas as pd

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
    'זהב Plus500': 'XAU/USD',
    'נפט Plus500': 'XTI/USD',
    'מדד US Tech 100': '^NDX'
}

times = ['1 דקה', '5 דקות', '10 דקות', '30 דקות', 'שעה', 'יום', 'שבוע']

selected_stock = st.selectbox("בחר נכס", list(stocks.keys()))
selected_time = st.selectbox("בחר טווח זמן", times)
amount = st.number_input("סכום השקעה ($)", min_value=1, step=1, value=1000)

def get_prediction(ticker):
    data = yf.download(ticker, period='1d', interval='1m')
    if data.empty or 'Close' not in data:
        return None, None, None, "אין נתוני סגירה"

    data['SMA5'] = data['Close'].rolling(window=5).mean()
    data['SMA20'] = data['Close'].rolling(window=20).mean()
    sma5 = data['SMA5'].iloc[-1]
    sma20 = data['SMA20'].iloc[-1]
    current = data['Close'].iloc[-1]

    trend = "קנייה 🔼" if sma5 > sma20 else "מכירה 🔽"
    diff_percent = (sma5 - sma20) / current
    predicted = current * (1 + diff_percent) if trend == "קנייה 🔼" else current * (1 - abs(diff_percent))

    return current, predicted, trend, None

if st.button("קבל תחזית"):
    try:
        ticker = stocks[selected_stock]
        current_price, predicted_price, trend, error = get_prediction(ticker)
        if error:
            st.error(error)
        else:
            profit = predicted_price * amount / current_price - amount
            st.success(f"תחזית ל-{selected_stock} בטווח {selected_time}: {trend}")
            st.info(f'רווח/הפסד צפוי: ${profit:.2f} (סה"כ: ${amount + profit:.2f})')
    except Exception as e:
        st.error(f"אירעה שגיאה: {str(e)}")
