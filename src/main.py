import streamlit as st
import pandas as pd
from ga_operation import jalankan_evolusi


st.set_page_config(layout="wide")

KEBUTUHAN_POSKO_DEFAULT = [
    {'nama': 'Posko A (Sekolah Sigma)', 'kebutuhan_relawan': 10, 'kebutuhan_truk': 3, 'kebutuhan_paket': 100},
    {'nama': 'Posko B (Balai Desa Vienna)', 'kebutuhan_relawan': 14, 'kebutuhan_truk': 4, 'kebutuhan_paket': 150},
    {'nama': 'Posko C (Lapangan Almuslim)', 'kebutuhan_relawan': 9,  'kebutuhan_truk': 2, 'kebutuhan_paket': 80}
]

SUMBER_DAYA_AWAL = {
    'total_relawan': 25,
    'total_truk': 8,
    'total_paket': 300
}

st.sidebar.header("⚙️ Atur Parameter Algoritma")
UKURAN_POPULASI = st.sidebar.slider("Ukuran Populasi", 10, 200, 50, 10)
JUMLAH_GENERASI = st.sidebar.slider("Jumlah Generasi", 10, 500, 100, 10)
TINGKAT_MUTASI = st.sidebar.slider("Tingkat Mutasi", 0.01, 1.0, 0.1, 0.01)
JUMLAH_ELIT = st.sidebar.slider("Jumlah Individu Elit", 1, 10, 2, 1)

st.sidebar.header("📦 Atur Sumber Daya Tersedia")
total_relawan_input = st.sidebar.number_input("Total Relawan", min_value=1, value=SUMBER_DAYA_AWAL['total_relawan'])
total_truk_input = st.sidebar.number_input("Total Truk", min_value=1, value=SUMBER_DAYA_AWAL['total_truk'])
total_paket_input = st.sidebar.number_input("Total Paket Bantuan", min_value=1, value=SUMBER_DAYA_AWAL['total_paket'])

SUMBER_DAYA = {
    'total_relawan': total_relawan_input,
    'total_truk': total_truk_input,
    'total_paket': total_paket_input
}

# Main menu
st.title("🔬 Visualisasi Algoritma Genetika")
st.write("**Kasus:** Optimisasi Distribusi Bantuan Bencana")

with st.expander("📂 Gunakan Dataset Kustom (Opsional)"):
    uploaded_file = st.file_uploader("Unggah file CSV Kebutuhan", type="csv")
    st.info("Format CSV harus memiliki kolom: `nama`, `kebutuhan_relawan`, `kebutuhan_truk`, `kebutuhan_paket`.")

try:
    if uploaded_file is not None:
        df_kebutuhan = pd.read_csv(uploaded_file)
        KEBUTUHAN_POSKO = df_kebutuhan.to_dict('records')
        st.sidebar.success("Dataset kustom berhasil dimuat!")
    else:
        KEBUTUHAN_POSKO = KEBUTUHAN_POSKO_DEFAULT
except Exception as e:
    st.error(f"Gagal memuat file CSV: {e}")
    st.stop()

with st.expander("Lihat Detail Masalah (Dataset Aktif)"):
    st.subheader("Kebutuhan Setiap Posko")
    st.table(pd.DataFrame(KEBUTUHAN_POSKO).set_index('nama'))
    st.subheader("Sumber Daya Tersedia")
    st.json(SUMBER_DAYA)

# Output
if st.button("🚀 Jalankan Simulasi Evolusi"):
    
    # Siapkan elemen UI untuk update live
    progress_chart = st.line_chart()
    progress_text = st.empty()
    st.subheader("🏆 Solusi Distribusi Optimal yang Ditemukan")
    results_placeholder = st.empty()

    def update_progress(generasi, total_generasi, riwayat_kebugaran):
        # Callback function untuk mengupdate UI dari dalam loop evolusi
        df_chart = pd.DataFrame({
            'Generasi': range(generasi),
            'Skor Kebugaran Terbaik': riwayat_kebugaran
        }).set_index('Generasi')
        progress_chart.line_chart(df_chart)
        progress_text.text(f"Memproses Generasi {generasi}/{total_generasi}...")

    with st.spinner("Komputer sedang melakukan 'evolusi'..."):
        # Panggil fungsi evolusi terpusat dari file logika
        solusi_terbaik, skor_terbaik, riwayat_kebugaran = jalankan_evolusi(
            kebutuhan_posko=KEBUTUHAN_POSKO,
            sumber_daya=SUMBER_DAYA,
            ukuran_populasi=UKURAN_POPULASI,
            jumlah_generasi=JUMLAH_GENERASI,
            tingkat_mutasi=TINGKAT_MUTASI,
            jumlah_elit=JUMLAH_ELIT,
            progress_callback=update_progress # Kirim fungsi update UI
        )
    
    st.success("Simulasi Selesai! 🔥")
    progress_text.text(f"Simulasi selesai setelah {JUMLAH_GENERASI} generasi.")

    # Tampilkan hasil akhir di placeholder
    with results_placeholder.container():
        total_alokasi_relawan, total_alokasi_truk, total_alokasi_paket = 0, 0, 0
        
        for i, posko in enumerate(KEBUTUHAN_POSKO):
            alokasi_relawan = solusi_terbaik[i*3]
            alokasi_truk = solusi_terbaik[i*3 + 1]
            alokasi_paket = solusi_terbaik[i*3 + 2]
            total_alokasi_relawan += alokasi_relawan
            total_alokasi_truk += alokasi_truk
            total_alokasi_paket += alokasi_paket
            
            st.write(f"**{posko['nama']}**:")
            st.write(f"  - **Relawan:** {alokasi_relawan} (kebutuhan: {posko['kebutuhan_relawan']})")
            st.write(f"  - **Truk:** {alokasi_truk} (kebutuhan: {posko['kebutuhan_truk']})")
            st.write(f"  - **Paket Bantuan:** {alokasi_paket} (kebutuhan: {posko['kebutuhan_paket']})")
            
        st.info(f"**Total Alokasi:** {total_alokasi_relawan} relawan, {total_alokasi_truk} truk, dan {total_alokasi_paket} paket bantuan.")
        st.metric(label="Skor Kebugaran Final", value=f"{skor_terbaik:.4f}")
