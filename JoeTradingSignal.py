import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Joe Trading Signal Pro", layout="wide")

# --- 2. SISTEM KEAMANAN (PASSWORD) ---
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

if not st.session_state['auth']:
    st.markdown("""
        <style>
        .auth-container {
            background-color: #1e1e26;
            padding: 30px;
            border-radius: 15px;
            border: 1px solid #3e3e4a;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🔐 Akses Terbatas")
    with st.container():
        pwd = st.text_input("Masukkan Password Dashboard:", type="password")
        if st.button("Buka Dashboard"):
            if pwd == "ADMIN123":
                st.session_state['auth'] = True
                st.rerun()
            else:
                st.error("Password Salah! Silakan hubungi Admin.")
    st.stop()

# --- 3. FUNGSI AMBIL DATA ASLI (REAL-TIME) ---
@st.cache_data(ttl=300)
def get_market_data(ticker):
    # Mengambil data 60 hari terakhir untuk menghitung MA
    df = yf.download(ticker, period="60d", interval="1d")
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()
    # Hitung RSI sederhana
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

# --- 4. HEADER DASHBOARD ---
st.title("📊 Joe Trading Signal Pro")
st.write(f"Update Terakhir: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} WIB")

# Pilihan Asset
asset_choice = st.selectbox(
    "Pilih Instrumen Market:", 
    ["GC=F", "BTC-USD", "DOGE-USD"], 
    format_func=lambda x: "GOLD (XAUUSD)" if x=="GC=F" else ("BITCOIN" if x=="BTC-USD" else "DOGECOIN")
)

# Load Data
data = get_market_data(asset_choice)
curr_price = data['Close'].iloc[-1]
prev_price = data['Close'].iloc[-2]
change = curr_price - prev_price
ma20_now = data['MA20'].iloc[-1]
ma50_now = data['MA50'].iloc[-1]
rsi_now = data['RSI'].iloc[-1]

# --- 5. TAMPILAN METRIC HARGA ---
col1, col2, col3 = st.columns(3)
col1.metric("Harga Running", f"${curr_price:,.2f}", f"{change:,.2f}")
col2.metric("MA 20 (Short)", f"{ma20_now:,.2f}")
col3.metric("MA 50 (Long)", f"{ma50_now:,.2f}")

# --- 6. LOGIKA SINYAL (MA CROSSOVER) ---
if ma20_now > ma50_now:
    signal_text = "STRONG BUY"
    signal_color = "#00ff00" # Hijau
    advice = "Harga di atas MA 20 & 50. Tren sedang BULLISH kuat."
elif ma20_now < ma50_now:
    signal_text = "STRONG SELL"
    signal_color = "#ff0000" # Merah
    advice = "Harga di bawah MA 20 & 50. Tren sedang BEARISH kuat."
else:
    signal_text = "WAIT / NEUTRAL"
    signal_color = "#888888" # Abu-abu
    advice = "Market sedang Sideways. Tunggu konfirmasi breakout."

st.markdown(f"""
    <div style="background-color:{signal_color}; padding:25px; border-radius:15px; text-align:center; margin-bottom:20px;">
        <h1 style="color:black; margin:0;">SINYAL: {signal_text}</h1>
        <p style="color:black; font-weight:bold;">{advice}</p>
    </div>
""", unsafe_allow_html=True)

# --- 7. GRAFIK INTERAKTIF ---
fig = go.Figure()

# Candlestick atau Line (Kita pakai Line agar bersih)
fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Price', line=dict(color='white', width=2)))
fig.add_trace(go.Scatter(x=data.index, y=data['MA20'], name='MA 20', line=dict(color='cyan', width=1.5)))
fig.add_trace(go.Scatter(x=data.index, y=data['MA50'], name='MA 50', line=dict(color='orange', width=1.5)))

fig.update_layout(
    template="plotly_dark",
    height=600,
    xaxis_title="Tanggal",
    yaxis_title="Price",
    margin=dict(l=20, r=20, t=20, b=20)
)
st.plotly_chart(fig, use_container_width=True)

st.info("💡 Tips: Gunakan sinyal ini sebagai alat bantu. Tetap perhatikan Money Management (DCA/Martingale) seperti strategi Bapak biasanya.")
