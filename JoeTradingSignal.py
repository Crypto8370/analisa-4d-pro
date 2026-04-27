import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Pro-Signal Predictor", layout="wide")

# Password sederhana (Sama seperti kemarin)
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

if not st.session_state['auth']:
    st.title("🔐 Akses Terbatas")
    pwd = st.text_input("Password Dashboard:", type="password")
    if st.button("Buka Dashboard"):
        if pwd == "ADMIN123":
            st.session_state['auth'] = True
            st.rerun()
        else:
            st.error("Password Salah!")
    st.stop()

# --- TAMPILAN DASHBOARD ---
st.title("📊 Pro-Signal Predictor")
asset = st.selectbox("Pilih Asset:", ["GC=F", "BTC-USD", "DOGE-USD"], format_func=lambda x: "XAUUSD (Gold)" if x=="GC=F" else x)

# Fungsi ambil data asli
@st.cache_data(ttl=300)
def get_real_data(ticker):
    df = yf.download(ticker, period="60d", interval="1d")
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()
    return df

data = get_real_data(asset)
curr_price = data['Close'].iloc[-1]
ma20 = data['MA20'].iloc[-1]
ma50 = data['MA50'].iloc[-1]

# Logika Sinyal Sederhana
status = "NEUTRAL"
color = "gray"
if ma20 > ma50:
    status = "BUY"
    color = "green"
elif ma20 < ma50:
    status = "SELL"
    color = "red"

st.metric("Harga Saat Ini", f"${curr_price:,.2f}")

# Card Sinyal
st.markdown(f"""
<div style="background-color:{color}; padding:20px; border-radius:10px; text-align:center; color:white;">
    <h1>SIGNAL: {status}</h1>
    <p>Strategi: MA Cross (Real-time Data)</p>
</div>
""", unsafe_allow_html=True)

# Grafik Real-time
fig = go.Figure()
fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Price', line=dict(color='white')))
fig.add_trace(go.Scatter(x=data.index, y=data['MA20'], name='MA 20', line=dict(color='cyan')))
fig.add_trace(go.Scatter(x=data.index, y=data['MA50'], name='MA 50', line=dict(color='orange')))
fig.update_layout(template="plotly_dark", height=500)
st.plotly_chart(fig, use_container_width=True)

st.write(f"Terakhir Update: {datetime.now().strftime('%H:%M:%S')} WIB")
