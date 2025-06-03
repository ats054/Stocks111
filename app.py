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
    'נפט גולמי': 'CL=F'
}

time_mapping = {
    '1 דקה': ('1d', '1m'),
    '5 דקות': ('1d', '5m'),
    '10 דקות': ('1d', '10m'),
    '30 דקות': ('1d', '30m'),
    'שעה': ('5d', '60m'),
    'יום': ('1mo', '1d'),
    'שבוע': ('3mo', '1wk')
}

selected_stock = st.selectbox("בחר נכס", list(stocks.keys()))
selected_time = st.selectbox("בחר טווח זמן", list(time_mapping.keys()))
amount = st.number_input("סכום השקעה ($)", min_value=1, step=1, value=1000)

def get_trend(data):
    data['SMA5'] = data['Close'].rolling(window=5).mean()
    data['SMA20'] = data['Close'].rolling(window=20).mean()
    if pd.isna(data['SMA5'].iloc[-1]) or pd.isna(data['SMA20'].iloc[-1]):
        return "נתונים לא מספקים", 0
    if data['SMA5'].iloc[-1] > data['SMA20'].iloc[-1]:
        return "קנייה 🔼", 1.02
    else:
        return "מכירה 🔽", 0.98

if st.button("קבל תחזית"):
    try:
        ticker = stocks[selected_stock]
        period, interval = time_mapping[selected_time]
        data = yf.download(ticker, period=period, interval=interval)
        if data.empty or 'Close' not in data:
            raise ValueError("אין נתוני סגירה זמינים")

        trend, multiplier = get_trend(data)
        current_price = data['Close'].iloc[-1]
        predicted_price = current_price * multiplier
        profit = predicted_price * amount / current_price - amount

        st.success(f"בטווח {selected_time}: {trend} תחזית ל-{selected_stock}")
        st.info(f'רווח/הפסד צפוי: ${profit:.2f} | סכום סופי: ${amount + profit:.2f}')

        # הצגת גרף
        fig, ax = plt.subplots()
        data['Close'].plot(ax=ax, label='מחיר נוכחי', color='blue')
        data['SMA5'].plot(ax=ax, label='SMA5', linestyle='--')
        data['SMA20'].plot(ax=ax, label='SMA20', linestyle='--')
        ax.legend()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"אירעה שגיאה בחיזוי הנתונים: {str(e)}")
