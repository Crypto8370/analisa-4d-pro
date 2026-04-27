import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# 1. SETTING
st.set_page_config(page_title="Joe Signal", layout="wide")

# 2. LOGIN
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

if not st.session_state['auth']:
    st.title("🔐 Login")
    pwd = st.text_input("Password:", type="password")
    if st.button("Masuk"):
        if pwd == "ADMIN123":
            st.session_state['auth'] = True
            st.rerun()
        st.stop()

# 3. KONTEN
st.title("📊 Joe Trading Signal")
pilih = st.selectbox("Market:", ["GC=F", "BTC-USD"])

try:
    df = yf.download(pilih, period="60d")
    df['MA20'] = df['Close'].rolling(20).mean()
    df['MA50'] = df['Close'].rolling(50).mean()
    
    hrg = df['Close'].iloc[-1]
    st.metric("Harga Saat Ini", f"${hrg:,.2f}")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Price'))
    fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], name='MA20'))
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig)

except Exception as e:
    st.error(f"Error: {e}")
