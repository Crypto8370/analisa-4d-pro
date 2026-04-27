import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# 1. SETTING UTAMA
st.set_page_config(page_title="Joe Signal Pro", layout="wide")

# 2. LOGIN (Sederhana agar tidak bentrok)
st.sidebar.title("🔐 Akses")
password = st.sidebar.text_input("Password:", type="password")

if password == "ADMIN123":
    st.title("📊 Joe Trading Signal Pro")
    asset = st.selectbox("Pilih Market:", ["GC=F", "BTC-USD"], format_func=lambda x: "GOLD (XAUUSD)" if x=="GC=F" else x)

    # 3. AMBIL DATA & ANALISA
    try:
        data = yf.download(asset, period="60d", interval="1d")
        
        if not data.empty:
            # Hitung MA 20 & 50
            data['MA20'] = data['Close'].rolling(window=20).mean()
            data['MA50'] = data['Close'].rolling(window=50).mean()
            
            last_price = data['Close'].iloc[-1]
            m20 = data['MA20'].iloc[-1]
            m50 = data['MA50'].iloc[-1]

            # 4. TAMPILAN SINYAL (Strategi Konsisten)
            col1, col2 = st.columns(2)
            col1.metric("Harga Running", f"${last_price:,.2f}")
            
            if m20 > m50:
                st.success("🚀 STATUS: STRONG BUY (Golden Cross)")
            else:
                st.error("📉 STATUS: STRONG SELL (Death Cross)")

            # 5. GRAFIK ANALISA
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Price', line=dict(color='white')))
            fig.add_trace(go.Scatter(x=data.index, y=data['MA20'], name='MA 20', line=dict(color='cyan')))
            fig.add_trace(go.Scatter(x=data.index, y=data['MA50'], name='MA 50', line=dict(color='orange')))
            fig.update_layout(template="plotly_dark", height=500, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.warning("Menunggu data market...")

    except Exception as e:
        st.error(f"Koneksi terganggu: {e}")

else:
    st.info("Silakan masukkan password di menu samping (Sidebar) untuk memulai.")
