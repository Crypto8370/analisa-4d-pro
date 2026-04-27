import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="Joe Signal", layout="wide")

# LOGIN
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

# KONTEN
st.title("📊 Joe Trading Signal")
pilih = st.selectbox("Market:", ["GC=F", "BTC-USD"])

try:
    df = yf.download(pilih, period="60d")
    df['MA20'] = df['Close'].rolling(20).mean()
    
    st.metric("Harga", f"${df['Close'].iloc[-1]:,.2f}")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Price'))
    fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], name='MA20'))
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig)
except Exception as e:
    st.error(f"Error: {e}")
