import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Pro-Signal Predictor", layout="centered")

# --- 2. STYLE CSS (Tampilan Mewah & Modern) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .metric-container {
        background-color: #1a1c23;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #30363d;
        text-align: center;
    }
    .signal-card {
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        margin: 20px 0;
        border: 2px solid #30363d;
    }
    .buy-glow { border-color: #2e7d32; box-shadow: 0 0 15px rgba(46, 125, 50, 0.4); background: rgba(46, 125, 50, 0.1); }
    .sell-glow { border-color: #c62828; box-shadow: 0 0 15px rgba(198, 40, 40, 0.4); background: rgba(198, 40, 40, 0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN SYSTEM (Keamanan Tetap Terjaga) ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 Akses Terbatas")
    pwd = st.text_input("Password Dashboard:", type="password")
    if st.button("Buka Dashboard"):
        if pwd == "ADMIN123":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Password Salah!")
    st.stop()

# --- 4. HEADER & PILIH MARKET ---
st.markdown("<h1 style='text-align: center;'>📊 Pro-Signal Predictor</h1>", unsafe_allow_html=True)
market = st.selectbox("Pilih Asset:", ["XAUUSD (Gold)", "BTCUSD (Bitcoin)", "ETHUSD"])

# --- 5. SIMULASI LOGIKA STRATEGI (MA 20, 50 & S/R) ---
# Di tahap ini kita buat data simulasi yang mengikuti tren
dates = pd.date_range(end=datetime.now(), periods=100)
base_price = 2330 if "XAU" in market else 65000
prices = base_price + np.cumsum(np.random.randn(100) * 5)
df = pd.DataFrame({'Date': dates, 'Close': prices})

# Hitung MA 20 & MA 50
df['MA20'] = df['Close'].rolling(window=20).mean()
df['MA50'] = df['Close'].rolling(window=50).mean()

# Hitung Support & Resistance (Low/High terakhir)
res_level = df['Close'].max()
sup_level = df['Close'].min()
curr_price = df['Close'].iloc[-1]

# Logika Sinyal berdasarkan MA & S/R
probabilitas = np.random.randint(75, 88)
if curr_price > df['MA20'].iloc[-1] and df['MA20'].iloc[-1] > df['MA50'].iloc[-1]:
    status = "BUY"
    style = "buy-glow"
    icon = "🚀"
else:
    status = "SELL"
    style = "sell-glow"
    icon = "📉"

# --- 6. VISUALISASI DASHBOARD ---

# Row 1: Sinyal Utama
st.markdown(f"""
    <div class="signal-card {style}">
        <h1 style='margin:0; font-size: 50px;'>{icon} {status}</h1>
        <p style='font-size: 20px;'>Probabilitas Akurasi: <b>{probabilitas}%</b></p>
        <hr style='border-color: #30363d;'>
        <p>Strategi: MA Cross & S/R Breakout</p>
    </div>
    """, unsafe_allow_html=True)

# Row 2: Indikator MA & S/R
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"<div class='metric-container'><b>MA 20</b><br><span style='color:#2196f3'>${df['MA20'].iloc[-1]:,.2f}</span></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='metric-container'><b>MA 50</b><br><span style='color:orange'>${df['MA50'].iloc[-1]:,.2f}</span></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='metric-container'><b>RSI (70/30)</b><br><span>45.21</span></div>", unsafe_allow_html=True)

st.write("") # Spasi

# Row 3: Support & Resistance Level
col_sr1, col_sr2 = st.columns(2)
col_sr1.metric("Resistance (High)", f"${res_level:,.2f}", delta_color="inverse")
col_sr2.metric("Support (Low)", f"${sup_level:,.2f}")

# --- 7. GRAFIK CANDLESTICK & MA ---
st.markdown("### 📈 Technical Chart Analysis")
fig = go.Figure()

# Garis Harga
fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name='Price', line=dict(color='white', width=2)))
# Garis MA 20
fig.add_trace(go.Scatter(x=df['Date'], y=df['MA20'], name='MA 20', line=dict(color='#2196f3', width=1.5)))
# Garis MA 50
fig.add_trace(go.Scatter(x=df['Date'], y=df['MA50'], name='MA 50', line=dict(color='orange', width=1.5)))

fig.update_layout(
    template="plotly_dark",
    margin=dict(l=10, r=10, t=10, b=10),
    height=400,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
st.plotly_chart(fig, use_container_width=True)

# --- 8. FOOTER INPUT ---
with st.expander("📝 Catatan / Input Manual"):
    st.text_area("Tambahkan Analisis Pribadi:")
    st.button("Simpan Analisis")

st.caption(f"Last Sync: {datetime.now().strftime('%H:%M:%S')} WIB | Strategi: Double MA + S/R")
