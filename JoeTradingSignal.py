import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# 1. KONFIGURASI DASHBOARD
st.set_page_config(page_title="Joe Signal Pro", layout="wide")

# 2. SISTEM LOGIN
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

if not st.session_state['auth']:
    st.title("🔐 Akses Joe Trading Signal")
    pwd = st.text_input("Password:", type="password")
    if st.button("Masuk"):
        if pwd == "ADMIN123":
            st.session_state['auth'] = True
            st.rerun()
    st.stop()

# 3. ANALISA STRATEGI MA 20/50
st.title("📊 Joe Trading Signal")
pilih = st.selectbox("Pilih Market:", ["GC=F", "BTC-USD"], format_func=lambda x: "GOLD (XAUUSD)" if x=="GC=F" else x)

try:
    # Ambil Data
    df = yf.download(pilih, period="60d", interval="1d")
    
    # Kalkulasi Indikator
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()
    
    harga_skrg = df['Close'].iloc[-1]
    m20 = df['MA20'].iloc[-1]
    m50 = df['MA50'].iloc[-1]

    # Tampilan Sinyal Berdasarkan Strategi
    if m20 > m50:
        st.success(f"🚀 SINYAL: BUY | Harga: ${harga_skrg:,.2f}")
        st.write("Keterangan: Tren Bullish (MA20 di atas MA50)")
    else:
        st.error(f"📉 SINYAL: SELL | Harga: ${harga_skrg:,.2f}")
        st.write("Keterangan: Tren Bearish (MA20 di bawah MA50)")

    # 4. GRAFIK INTERAKTIF
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Price', line=dict(color='white')))
    fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], name='MA 20', line=dict(color='cyan')))
    fig.add_trace(go.Scatter(x=df.index, y=df['MA50'], name='MA 50', line=dict(color='orange')))
    fig.update_layout(template="plotly_dark", height=500)
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Gagal mengambil data: {e}")
