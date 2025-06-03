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

if st.button("קבל תחזית"):
    try:
        # הגדרת הטיקר מתוך הבחירה
        ticker = stocks[selected_stock]

        # הורדת נתונים
        data = yf.download(ticker, period='1d', interval='1m')

        if data.empty or 'Close' not in data.columns:
            raise ValueError("אין נתוני סגירה זמינים")

        # חישוב ממוצעים נעים
        data['SMA5'] = data['Close'].rolling(window=5).mean()
        data['SMA20'] = data['Close'].rolling(window=20).mean()

        current_price = data['Close'].iloc[-1]

        if pd.isna(data['SMA5'].iloc[-1]) or pd.isna(data['SMA20'].iloc[-1]):
            trend = "נתונים לא מספיקים למגמה"
        elif data['SMA5'].iloc[-1] > data['SMA20'].iloc[-1]:
            trend = "קנייה 🔼"
        else:
            trend = "מכירה 🔽"

        predicted_price = current_price * (1.01 if "קנייה" in trend else 0.99)
        profit = predicted_price * amount / current_price - amount

        st.success(f"תחזית ל-{selected_stock} בטווח {selected_time}: {trend}")
        st.info(f'רווח/הפסד צפוי: ${profit:.2f} (סה"כ: ${amount + profit:.2f})')
        st.line_chart(data['Close'])

    except Exception as e:
        st.error(f"שגיאה: {str(e)}")
