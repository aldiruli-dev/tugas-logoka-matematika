import streamlit as st
import pandas as pd
import itertools
import time

# =======================
# 1. KONFIGURASI HALAMAN
# =======================
st.set_page_config(
    page_title="sistem keputusan sirkulasi perpustakaan",
    page_icon="🧠",
    layout="wide"
)

# =======================
# 2. CSS PREMIUM (NEON DARK MODE)
# =======================
st.markdown("""
<style>
    .stApp {
        background-color: #0b0e14 !important;
        color: #d1d5db !important;
    }
    
    /* Card Glassmorphism */
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
    }

    .main-title {
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 32px;
    }

    /* Result Banners */
    .banner {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        font-size: 1.1rem;
        border-left: 8px solid;
    }
    .approved { background: rgba(16, 185, 129, 0.1); color: #10b981; border-left-color: #10b981; }
    .denied { background: rgba(239, 68, 68, 0.1); color: #ef4444; border-left-color: #ef4444; }
</style>
""", unsafe_allow_html=True)

# =======================
# 3. SIDEBAR (CONTROL CENTER)
# =======================
with st.sidebar:
    st.markdown("<h2 class='main-title'>Panel Kontrol petugas</h2>", unsafe_allow_html=True)
    st.write("---")
    
    with st.expander("👤 Identitas Peminjam", expanded=True):
        nama = st.text_input("Nama Lengkap", "Rizky Ramadhan")
        kategori_user = st.selectbox("Level Anggota", ["Mahasiswa", "Dosen", "Umum"])
    
    with st.expander("📖 Detail Koleksi", expanded=True):
        buku = st.text_input("Judul Buku", "Struktur Data & Logika")
        tipe_buku = st.radio("Kategori Buku", ["Sirkulasi (Bisa Pinjam)", "Referensi (Baca di Tempat)"])
    
    st.write("---")
    st.markdown("*Status Proposisi:*")
    A = st.toggle("Keanggotaan Aktif (A)", value=True)
    B = st.toggle("Buku Tersedia (B)", value=True)
    C = st.toggle("Bebas Denda (C)", value=True)
    D = st.toggle("Dispensasi/Izin Khusus (D)", value=False)

# =======================
# 4. LOGIKA PROPOSISIONAL BERLAPIS
# =======================
# Logika 1: Syarat Dasar
is_referensi = (tipe_buku == "Referensi (Baca di Tempat)")
# Logika 2: Rumus Utama (A ∧ B) ∧ (C ∨ D)
aturan_utama = (A and B) and (C or D)
# Keputusan Akhir: Tidak boleh referensi AND harus memenuhi aturan utama
final_decision = aturan_utama and not is_referensi

# =======================
# 5. MAIN DASHBOARD
# =======================
st.markdown("<h1 class='main-title'>Sistem Keputusan Sirkulasi Perpustakaan</h1>", unsafe_allow_html=True)

# Row 1: Metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric("Kategori User", kategori_user)
m2.metric("Status Sistem", "ONLINE", delta="Stable")
m3.metric("Logika Terproses", "64 Combinations")
m4.metric("Denda Terdeteksi", "Rp 0" if C else "Rp 15.000")

st.markdown("<br>", unsafe_allow_html=True)

# Row 2: Analysis & Action
col_l, col_r = st.columns([1.5, 1])

with col_l:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("🔍 Analisis Kelayakan Pinjam")
    
    if st.button("🚀 JALANKAN VALIDASI SISTEM"):
        with st.spinner('Mengevaluasi proposisi logika...'):
            time.sleep(1)
            if final_decision:
                st.markdown(f"<div class='banner approved'>✅ STATUS: PEMINJAMAN DISETUJUI<br><small>Buku '{buku}' dapat diproses untuk {nama}.</small></div>", unsafe_allow_html=True)
                st.balloons()
            else:
                st.markdown("<div class='banner denied'>❌ STATUS: PEMINJAMAN DITOLAK</div>", unsafe_allow_html=True)
                if is_referensi: st.error("Alasan: Buku kategori 'Referensi' tidak diizinkan dibawa pulang.")
                elif not (C or D): st.error("Alasan: Anggota memiliki denda tertunggak tanpa surat dispensasi.")
                else: st.warning("Alasan: Masalah pada ketersediaan koleksi atau status keanggotaan.")
    st.markdown("</div>", unsafe_allow_html=True)

    # Tabel Matrix
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📊 Matrix Logika Proposisional")
    data = []
    for a, b, c in itertools.product([1, 0], repeat=3):
        res = "ALLOWED" if (a and b and c) else "DENIED"
        data.append([a, b, c, res])
    df = pd.DataFrame(data, columns=["Aktif (A)", "Ready (B)", "No Debt (C)", "Status"])
    st.dataframe(df, use_container_width=True, height=200)
    st.markdown("</div>", unsafe_allow_html=True)

with col_r:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("⚙️ Alur Logika Keputusan")
    st.latex(r"P = ((A \land B) \land (C \lor D)) \land \neg R")
    st.caption("R = Kategori Referensi (Restricted)")
    
    

    st.markdown("""
    *Arsitektur Keputusan:*
    1. *Layer 1*: Validasi fisik (Buku & User).
    2. *Layer 2*: Validasi administratif (Denda & Izin).
    3. *Layer 3*: Filter kategori (Referensi Lock).
    """)
    st.markdown("</div>", unsafe_allow_html=True)

    # Grafik Statistik (Bar Chart)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📈 Tren Peminjaman")
    chart_data = pd.DataFrame({
        'Hari': ['Sen', 'Sel', 'Rab', 'Kam', 'Jum'],
        'Jumlah': [15, 30, 25, 40, 20]
    })
    st.bar_chart(chart_data, x='Hari', y='Jumlah', color="#3b82f6")
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.write("---")
st.markdown("<p style='text-align:center; color:#4b5563;'>Enterprise Library Intelligence | Developed for Logic Class 2025</p>", unsafe_allow_html=True)