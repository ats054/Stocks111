import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

st.set_page_config(page_title="תחזית מניות וזהב - אמת", layout="centered")
st.title("📈 תחזית חכמה - מניות, זהב וקריפטו בזמן אמת")
st.write("בחר נכס, טווח זמן וסכום השקעה - וקבל תחזית מבוססת תנועה אמיתית + גרף")

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

interval_map = {
    '1 דקה': '1m',
    '5 דקות': '5m',
    '10 דקות': '10m',
    '30 דקות': '30m',
    'שעה': '60m',
    'יום': '1d',
    'שבוע': '1wk'
}

selected_stock = st.selectbox("בחר נכס", list(stocks.keys()))
selected_time = st.selectbox("בחר טווח זמן", list(interval_map.keys()))
amount = st.number_input("סכום השקעה ($)", min_value=1, step=1, value=1000)

def calculate_expected_return(data):
    data['return'] = data['Close'].pct_change()
    avg_return = data['return'].mean()
    std_dev = data['return'].std()
    expected_return_pct = avg_return * 100
    return expected_return_pct

if st.button("קבל תחזית"):
    try:
        ticker = stocks[selected_stock]
        interval = interval_map[selected_time]
        data = yf.download(ticker, period='5d', interval=interval)

        if data.empty or 'Close' not in data:
            raise ValueError("אין נתונים זמינים לנכס שנבחר.")

        st.subheader("📊 גרף תנועה אחרונה")
        st.line_chart(data['Close'])

        expected_return_pct = calculate_expected_return(data)
        predicted_profit = amount * expected_return_pct / 100
        final_amount = amount + predicted_profit

        recommendation = "קנייה 🔼" if expected_return_pct > 0 else "מכירה 🔽"
        st.success(f"תחזית ל-{selected_stock} בטווח {selected_time}: {recommendation}")
        st.info(f"תשואה צפויה: {expected_return_pct:.2f}%")
        st.info(f"רווח/הפסד צפוי: ${predicted_profit:.2f} (סה\"כ: ${final_amount:.2f})")

    except Exception as e:
        st.error(f"שגיאה בטעינת התחזית: {str(e)}")
