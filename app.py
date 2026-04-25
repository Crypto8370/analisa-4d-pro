import streamlit as st
import pandas as pd
import plotly.express as px
import random

# --- 1. SISTEM KEAMANAN ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False
    if st.session_state.password_correct:
        return True

    st.set_page_config(page_title="Login Akses", page_icon="🔐")
    st.title("🔐 Login Dashboard Analisis")
    password = st.text_input("Masukkan Password Anda:", type="password")
    if st.button("Masuk"):
        if password == "ADMIN123":
            st.session_state.password_correct = True
            st.rerun()
        else:
            st.error("❌ Password Salah!")
    return False

if not check_password():
    st.stop()

# --- 2. TAMPILAN UTAMA (BALIK KE GAYA AWAL) ---
st.set_page_config(page_title="4D Stats Pro", layout="centered")

st.title("📊 4D Pro-Stats Analyzer")
st.write("Sistem Analisis Statistik Berdasarkan Riwayat Data")

# Inisialisasi Data
if 'data_history' not in st.session_state:
    st.session_state.data_history = []

# PANEL INPUT DI TENAH (Gaya Awal)
st.subheader("📥 Input Data Result")
new_data = st.text_input("Masukkan 4 Angka (Contoh: 9645):", max_chars=4)

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("➕ Tambah Data"):
        if len(new_data) == 4 and new_data.isdigit():
            st.session_state.data_history.append(new_data)
            st.success(f"Data {new_data} tersimpan!")
            st.rerun()
        else:
            st.error("Gunakan 4 angka!")
with col_btn2:
    if st.button("🗑️ Reset Semua"):
        st.session_state.data_history = []
        st.rerun()

st.markdown("---")

# --- 3. LOGIKA ANALISIS & REKOMENDASI ---
if st.session_state.data_history:
    semua_digit = "".join(st.session_state.data_history)
    counts = pd.Series(list(semua_digit)).value_counts().sort_index()
    
    # Ambil 7 Digit Terkuat untuk BBFS
    top_7 = list(counts.nlargest(7).index)
    bbfs_result = "".join(sorted(top_7))

    # TAMPILAN HASIL
    st.subheader("🎯 Hasil Rekomendasi Hari Ini")
    c1, c2, c3 = st.columns(3)
    c1.metric("BBFS (7D)", bbfs_result)
    
    # Rekomendasi Angka Jadi (Random dari Top Digit)
    if len(top_7) >= 4:
        r4d = "".join(random.sample(top_7, 4))
        r3d = "".join(random.sample(top_7, 3))
        r2d = "".join(random.sample(top_7, 2))
        c2.write(f"**Top 4D:** {r4d}")
        c2.write(f"**Top 3D:** {r3d}")
        c3.write(f"**Top 2D:** {r2d}")
        c3.write(f"**Total Data:** {len(st.session_state.data_history)} hari")

    st.markdown("---")
    
    # GRAFIK VISUAL
    st.subheader("📈 Visualisasi Frekuensi Digit")
    fig = px.bar(x=counts.index, y=counts.values, 
                 labels={'x':'Digit Angka', 'y':'Jumlah Muncul'},
                 color=counts.values, color_continuous_scale='Blues')
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("👋 Selamat Datang! Masukkan data result di atas untuk melihat analisis.")
