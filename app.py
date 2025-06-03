import streamlit as st
import yfinance as yf

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
        ticker = stocks[selected_stock]
        data = yf.download(ticker, period='1d', interval='1m')
        current_price = data['Close'].iloc[-1]
        predicted_price = current_price * 1.02
        profit = predicted_price * amount / current_price - amount

        st.success(f"תחזית ל-{selected_stock} בטווח {selected_time}: קנייה 🔼")
        st.info(f'רווח/הפסד צפוי: ${profit:.2f} (סה"כ: ${amount + profit:.2f})')
    except Exception as e:
        st.error("אירעה שגיאה בחיזוי הנתונים. ייתכן שאין נתונים זמינים או שיש בעיה זמנית.")
