import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="תחזית זהב, מניות וקריפטו", layout="centered")
st.title("🔮 תחזית חכמה - זהב, מניות, קריפטו ו־Plus500")
st.write("בחר נכס, טווח זמן וסכום השקעה - וקבל תחזית עם חיווי מיידי.")

# מניות ונכסים זמינים
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

# המרת טווחי זמן ל־yfinance
intervals = {
    '1 דקה': '1m',
    '5 דקות': '5m',
    '10 דקות': '15m',
    '30 דקות': '30m',
    'שעה': '60m',
    'יום': '1d',
    'שבוע': '1wk'
}

# בחירת נכס, זמן וסכום
selected_stock = st.selectbox("בחר נכס", list(stocks.keys()))
selected_time = st.selectbox("בחר טווח זמן", list(intervals.keys()))
amount = st.number_input("סכום השקעה ($)", min_value=1, step=1, value=1000)

# פונקציית זיהוי מגמה
def get_trend(data):
    data['SMA5'] = data['Close'].rolling(window=5).mean()
    data['SMA20'] = data['Close'].rolling(window=20).mean()
    if pd.isna(data['SMA5'].iloc[-1]) or pd.isna(data['SMA20'].iloc[-1]):
        return "לא ניתן לקבוע מגמה ❓"
    return "קנייה 🔼" if data['SMA5'].iloc[-1] > data['SMA20'].iloc[-1] else "מכירה 🔽"

# כאשר לוחצים על הכפתור
if st.button("קבל תחזית"):
    try:
        ticker = stocks[selected_stock]
        interval = intervals[selected_time]
        data = yf.download(ticker, period='1d', interval=interval)
        if data.empty or 'Close' not in data:
            raise ValueError("אין נתוני סגירה זמינים")

        current_price = data['Close'].iloc[-1]
        trend = get_trend(data)
        predicted_price = current_price * (1.01 if trend == "קנייה 🔼" else 0.99)
        profit = predicted_price * amount / current_price - amount

        st.line_chart(data['Close'])

        st.success(f"תחזית ל-{selected_stock} בטווח {selected_time}: {trend}")
        st.info(f'רווח/הפסד צפוי: ${profit:.2f} (סה"כ: ${amount + profit:.2f})')

    except Exception as e:
        st.error(f"אירעה שגיאה: {str(e)}")
