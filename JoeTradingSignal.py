import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# 1. SETTING HALAMAN
st.set_page_config(page_title="Joe Signal Pro", layout="wide")

# 2. LOGIN SEDERHANA
if 'cek' not in st.session_state:
    st.session_state['cek'] = False

if not st.session_state['cek']:
    st.title("🔐 Login Joe Signal")
    kunci = st.text_input("Password:", type="password")
    if st.button("Masuk"):
        if kunci == "ADMIN123":
            st.session_state['cek'] = True
            st.rerun()
        else:
            st.error("Salah Boss!")
    st.stop()

# 3. AMBIL DATA MARKET
st.title("📊 Joe Trading Signal")

pilih = st.selectbox("Pilih Market:", ["GC=F", "BTC-USD", "DOGE-USD"], 
                     format_func=lambda x: "GOLD (XAUUSD)" if x=="GC=F" else x)

@st.cache_data(ttl=60)
def ambil_data(simbol):
    d = yf.download(simbol, period="60d", interval="1d")
    d['MA20'] = d['Close'].rolling(20).mean()
    d['MA50'] = d['Close'].rolling(50).mean()
    return d

try:
    df = ambil_data(pilih)
    harga = df['Close'].iloc[-1]
    m20 = df['MA20'].iloc[-1]
    m50 = df['MA50'].iloc[-1]

    # 4. KOTAK SINYAL
    st.metric("Harga Saat Ini", f"${harga:,.2f}")
    
    if m20 > m50:
        st.success(f"🚀 SINYAL: BUY (Tren Naik)")
    else:
        st.error(f"📉 SINYAL: SELL (Tren Turun)")

    # 5. GRAFIK
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Harga'))
    fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], name='MA20'))
    fig.add_trace(go.Scatter(x=df.index, y=df['MA50'], name='MA50'))
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Koneksi Market Terputus: {e}")
