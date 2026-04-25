import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter

# 1. Konfigurasi Tampilan (Wide Layout & Dark Theme)
st.set_page_config(
    page_title="4D Pro-Stats Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk tampilan Dashboard yang lebih "Amazing"
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1f2937; padding: 20px; border-radius: 12px; border: 1px solid #374151; }
    .stAlert { border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Inisialisasi Database (Session State)
if 'data_4d' not in st.session_state:
    st.session_state.data_4d = []

# 3. Header Aplikasi
st.title("📊 4D Pro-Stats Analyzer & BBFS Logic")
st.write("Sistem Analisis Statistik Berdasarkan Riwayat Data Historis")

# 4. Sidebar: Input Result Harian
with st.sidebar:
    st.header("📥 Panel Input")
    st.write("Masukkan hasil result harian di sini.")
    
    result_input = st.text_input("Input 4 Angka (Contoh: 7129):", max_chars=4)
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("➕ Tambah Data"):
            if len(result_input) == 4 and result_input.isdigit():
                st.session_state.data_4d.append(result_input)
                st.success(f"Result {result_input} berhasil disimpan!")
            else:
                st.error("Masukkan 4 digit angka!")
    
    with col_btn2:
        if st.button("🗑️ Reset All"):
            st.session_state.data_4d = []
            st.rerun()

    st.divider()
    st.write(f"Total Data Terkumpul: **{len(st.session_state.data_4d)}** hari")

# 5. Logika Utama (Hanya berjalan jika ada data)
if len(st.session_state.data_4d) > 0:
    # Mengolah data menjadi DataFrame
    df = pd.DataFrame(st.session_state.data_4d, columns=['Full'])
    df['As'] = df['Full'].str[0].astype(int)
    df['Kop'] = df['Full'].str[1].astype(int)
    df['Kepala'] = df['Full'].str[2].astype(int)
    df['Ekor'] = df['Full'].str[3].astype(int)

    # A. Panel Atas: Prediksi & BBFS
    col_main, col_bbfs, col_mati = st.columns([2, 1, 1])

    with col_main:
        st.subheader("💡 Prediksi Angka Main (Posisi)")
        c1, c2, c3, c4 = st.columns(4)
        
        # Cari angka paling sering (Hot) di tiap posisi
        h_as = df['As'].value_counts().idxmax()
        h_kop = df['Kop'].value_counts().idxmax()
        h_kep = df['Kepala'].value_counts().idxmax()
        h_ekor = df['Ekor'].value_counts().idxmax()
        
        c1.metric("AS", h_as)
        c2.metric("KOP", h_kop)
        c3.metric("KEPALA", h_kep)
        c4.metric("EKOR", h_ekor)
        st.info(f"**Kombinasi Rekomendasi Jitu:** {h_as}{h_kop}{h_kep}{h_ekor}")

    with col_bbfs:
        st.subheader("🎲 BBFS 5 Digit")
        all_digits = "".join(st.session_state.data_4d)
        counts = Counter(all_digits)
        # Ambil 5 angka paling sering muncul secara global
        top_5 = [item[0] for item in counts.most_common(5)]
        top_5.sort()
        st.success(f"**Angka BBFS:**\n\n # {', '.join(top_5)}")

    with col_mati:
        st.subheader("⚠️ Angka Mati")
        # Cari angka yang paling jarang muncul (0-9)
        all_possible = [str(i) for i in range(10)]
        freq_map = {d: counts.get(d, 0) for d in all_possible}
        # Urutkan dari yang terkecil
        dead_numbers = sorted(freq_map.items(), key=lambda x: x[1])
        low_3 = [item[0] for item in dead_numbers[:3]]
        st.error(f"**Prediksi Lemah:**\n\n # {', '.join(low_3)}")

    st.divider()

    # B. Panel Tengah: Visualisasi Grafik
    st.subheader("📊 Distribusi Frekuensi Angka (0-9)")
    posisi = st.radio("Pilih Analisis Posisi:", ["As", "Kop", "Kepala", "Ekor"], horizontal=True)
    
    freq_df = df[posisi].value_counts().reset_index()
    freq_df.columns = ['Angka', 'Muncul']
    freq_df = freq_df.sort_values('Angka')

    fig = px.bar(
        freq_df, x='Angka', y='Muncul', 
        text='Muncul', color='Muncul',
        color_continuous_scale='Blues',
        title=f"Berapa Kali Angka Muncul di Posisi {posisi} (Total: {len(df)} data)"
    )
    st.plotly_chart(fig, use_container_width=True)

    # C. Tabel Riwayat
    with st.expander("📜 Lihat Semua Riwayat Data"):
        st.write(df.iloc[::-1]) # Tampilkan dari yang terbaru

else:
    st.info("👋 Selamat Datang! Silakan masukkan data histori result di sidebar untuk memulai analisis.")
