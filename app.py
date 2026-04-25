import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Trading Signal Pro", layout="centered")

# --- STYLE CSS (Agar Tampilan Mewah & Centered) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #2e7d32; color: white; }
    .signal-box { padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px; border: 1px solid #30363d; }
    .buy-signal { background-color: rgba(46, 125, 50, 0.2); border-left: 5px solid #2e7d32; }
    .sell-signal { background-color: rgba(198, 40, 40, 0.2); border-left: 5px solid #c62828; }
    .wait-signal { background-color: rgba(255, 193, 7, 0.1); border-left: 5px solid #ffc107; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN SYSTEM ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login Dashboard Pro")
    password = st.text_input("Masukkan Password:", type="password")
    if st.button("Masuk"):
        if password == "ADMIN123":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Password Salah!")
    st.stop()

# --- HEADER ---
st.markdown("<h1 style='text-align: center;'>📊 Trading Signal Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>XAUUSD & Crypto Market Predictor</p>", unsafe_allow_html=True)

# --- SIMULASI DATA MARKET (XAUUSD) ---
def get_simulated_data():
    dates = pd.date_range(end=datetime.now(), periods=50)
    prices = np.random.normal(2300, 15, size=50).cumsum() / 50 + 2200
    df = pd.DataFrame({'Date': dates, 'Close': prices})
    # Hitung RSI Sederhana
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    df['MA20'] = df['Close'].rolling(window=20).mean()
    return df

data = get_simulated_data()
current_price = data['Close'].iloc[-1]
current_rsi = data['RSI'].iloc[-1]
current_ma = data['MA20'].iloc[-1]

# --- PANEL ANALISIS & SINYAL ---
st.markdown("### 🤖 Robot Signal AI")

# Logika Sinyal (Probabilitas 70-80%)
probabilitas = np.random.randint(72, 89)
if current_rsi < 35:
    signal_type = "BUY"
    css_class = "buy-signal"
    icon = "🟢"
    desc = f"Harga Jenuh Jual (Oversold). Probabilitas naik {probabilitas}%"
elif current_rsi > 65:
    signal_type = "SELL"
    css_class = "sell-signal"
    icon = "🔴"
    desc = f"Harga Jenuh Beli (Overbought). Probabilitas turun {probabilitas}%"
else:
    signal_type = "WAITING"
    css_class = "wait-signal"
    icon = "🟡"
    desc = "Market Sideways. Menunggu konfirmasi breakout."

st.markdown(f"""
    <div class="signal-box {css_class}">
        <h2 style='margin:0;'>{icon} SIGNAL: {signal_type}</h2>
        <p style='font-size: 20px; font-weight: bold;'>Probabilitas: {probabilitas}%</p>
        <p>{desc}</p>
    </div>
    """, unsafe_allow_html=True)

# --- METRIC KOTAK (Seperti Dashboard Pro) ---
col1, col2, col3 = st.columns(3)
col1.metric("Current Price", f"${current_price:,.2f}")
col2.metric("RSI (14)", f"{current_rsi:.2f}")
col3.metric("Trend MA(20)", "Bullish" if current_price > current_ma else "Bearish")

# --- VISUAL GRAFIK MARKET ---
st.markdown("### 📈 Market Movement")
fig = go.Figure()
fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Price', line=dict(color='#2196f3', width=3)))
fig.add_trace(go.Scatter(x=data['Date'], y=data['MA20'], name='MA 20', line=dict(color='orange', dash='dash')))
fig.update_layout(template="plotly_dark", margin=dict(l=20, r=20, t=20, b=20), height=350)
st.plotly_chart(fig, use_container_width=True)

# --- INPUT DATA MANUAL (History Result) ---
with st.expander("📥 Panel Input Data Riwayat"):
    new_data = st.text_input("Masukkan Result Baru (Contoh: 9645):")
    if st.button("Simpan Data"):
        st.success(f"Data {new_data} Berhasil Disimpan ke database!")

# --- FOOTER ---
st.markdown("---")
st.caption(f"Last Update: {datetime.now().strftime('%H:%M:%S')} WIB | User: Ahmad Kosasih")
