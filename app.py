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
    'זהב Plus500': 'XAUUSD=X',
    'נפט Plus500': 'XTIUSD=X',
    'מדד US Tech 100': '^NDX'
}

interval_mapping = {
    '1 דקה': '1m',
    '5 דקות': '5m',
    '10 דקות': '15m',
    '30 דקות': '30m',
    'שעה': '60m',
    'יום': '1d',
    'שבוע': '1wk'
}

selected_stock = st.selectbox("בחר נכס", list(stocks.keys()))
selected_time_label = st.selectbox("בחר טווח זמן", list(interval_mapping.keys()))
amount = st.number_input("סכום השקעה ($)", min_value=1, step=1, value=1000)

def get_trend_and_profit(data, amount):
    data['SMA5'] = data['Close'].rolling(window=5).mean()
    data['SMA20'] = data['Close'].rolling(window=20).mean()

    if pd.isna(data['SMA5'].iloc[-1]) or pd.isna(data['SMA20'].iloc[-1]):
        return "נתונים לא מספיקים", 0.0, 0.0

    trend = "קנייה 🔼" if data['SMA5'].iloc[-1] > data['SMA20'].iloc[-1] else "מכירה 🔽"
    current_price = data['Close'].iloc[-1]
    predicted_price = current_price * (1.01 if trend == "קנייה 🔼" else 0.99)
    profit = (predicted_price - current_price) * (amount / current_price)
    total_value = amount + profit

    return trend, profit, total_value

if st.button("קבל תחזית"):
    try:
        interval = interval_mapping[selected_time_label]
        ticker = stocks[selected_stock]
        data = yf.download(ticker, period='1d', interval=interval)

        if data.empty or 'Close' not in data:
            raise ValueError("אין נתוני סגירה זמינים")

        trend, profit, total_value = get_trend_and_profit(data, amount)

        st.success(f"תחזית ל-{selected_stock} בטווח {selected_time_label}: {trend}")
        st.info(f'רווח/הפסד צפוי: ${profit:.2f} (סה"כ: ${total_value:.2f})')

        st.line_chart(data['Close'])

    except Exception as e:
        st.error(f"אירעה שגיאה בחיזוי הנתונים: {str(e)}")
