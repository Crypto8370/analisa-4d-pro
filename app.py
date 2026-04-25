import streamlit as st
import pandas as pd
import plotly.express as px

# 1. FUNGSI KEAMANAN (LOGIN)
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    if st.session_state.password_correct:
        return True

    st.set_page_config(page_title="Akses Terbatas", page_icon="🔐")
    st.title("🔐 Login Dashboard Pro")
    password = st.text_input("Masukkan Password:", type="password")
    if st.button("Masuk"):
        if password == "ADMIN123": # <--- Boleh Bapak ganti sesuka hati
            st.session_state.password_correct = True
            st.rerun()
        else:
            st.error("❌ Password Salah!")
    return False

if not check_password():
    st.stop()

# 2. LANJUTAN KODING ANALISIS (SETELAH LOGIN)
st.set_page_config(page_title="4D Pro-Stats Analyzer", layout="wide")

st.title("📊 4D Pro-Stats Analyzer & BBFS Logic")
st.markdown("---")

# Inisialisasi Data
if 'data_history' not in st.session_state:
    st.session_state.data_history = []

# SIDEBAR UNTUK INPUT
with st.sidebar:
    st.header("📥 Panel Input")
    new_data = st.text_input("Input 4 Angka (Contoh: 7129):", max_chars=4)
    if st.button("➕ Tambah Data"):
        if len(new_data) == 4 and new_data.isdigit():
            st.session_state.data_history.append(new_data)
            st.success(f"Data {new_data} tersimpan!")
        else:
            st.error("Masukkan 4 angka!")
    
    if st.button("🗑️ Reset All"):
        st.session_state.data_history = []
        st.rerun()

# LOGIKA ANALISIS
if st.session_state.data_history:
    df = pd.DataFrame(st.session_state.data_history, columns=['Angka'])
    
    # Hitung Frekuensi Angka
    semua_digit = "".join(st.session_state.data_history)
    counts = pd.Series(list(semua_digit)).value_counts().sort_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Statistik Frekuensi")
        fig = px.bar(x=counts.index, y=counts.values, labels={'x':'Digit', 'y':'Muncul'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Rekomendasi BBFS")
        bbfs = list(counts.head(7).index) # Ambil 7 angka tersering
        st.info(f"**7 Digit Kuat:** {''.join(bbfs)}")
        
        st.subheader("🚫 Angka Mati (Jarang Muncul)")
        mati = [str(i) for i in range(10) if str(i) not in counts.index or counts[str(i)] == counts.min()]
        st.warning(f"**Digit Lemah:** {', '.join(mati)}")

else:
    st.info("👋 Selamat Datang! Silakan masukkan data di sidebar untuk memulai.")
