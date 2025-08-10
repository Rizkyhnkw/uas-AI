import streamlit as st
import random
import pandas as pd

# setup dataset
KEBUTUHAN_POSKO = [
    {'nama': 'Posko A (Sekolah sigma)', 'kebutuhan_relawan': 10, 'kebutuhan_truk': 3},
    {'nama': 'Posko B (Balai desa Vienna)', 'kebutuhan_relawan': 14, 'kebutuhan_truk': 4},
    {'nama': 'Posko C (Lapangan Almuslim)', 'kebutuhan_relawan': 9, 'kebutuhan_truk': 2},
]

SUMBER_DAYA = {
    'total_relawan': 25,
    'total_truk': 8
}

# ui & parameter
st.sidebar.header("Atur Parameter Algoritma⚙️")

# widget parameter
UKURAN_POPULASI = st.sidebar.slider("Ukuran Populasi", min_value=10, max_value=200, value=50, step=10)
JUMLAH_GENERASI = st.sidebar.slider("Jumlah Generasi", min_value=10, max_value=500, value=100, step=10)
TINGKAT_MUTASI = st.sidebar.slider("Tingkat Mutasi", min_value=0.01, max_value=1.0, value=0.1, step=0.01)
JUMLAH_ELIT = st.sidebar.slider("Jumlah Individu Elit (Elite Count)", min_value=1, max_value=10, value=2, step=1)

# Operasi Algoritma genetik
def buat_individu():
    kromosom = []
    for posko in KEBUTUHAN_POSKO:
        alokasi_relawan = random.randint(0, SUMBER_DAYA['total_relawan'])
        alokasi_truk = random.randint(0, SUMBER_DAYA['total_truk'])
        kromosom.extend([alokasi_relawan, alokasi_truk])
    return kromosom

def hitung_kebugaran(individu):
    total_alokasi_relawan = sum(individu[i] for i in range(0, len(individu), 2))
    # PERBAIKAN: Mengambil total alokasi truk dari indeks yang benar (1, 3, 5, ...)
    total_alokasi_truk = sum(individu[i] for i in range(1, len(individu), 2))

    # tunda jika alokasi > sumberdaya
    if total_alokasi_relawan > SUMBER_DAYA['total_relawan'] or total_alokasi_truk > SUMBER_DAYA['total_truk']:
        return 0

    # hitung total kekurangan
    total_kekurangan = 0
    for i, posko in enumerate(KEBUTUHAN_POSKO):
        alokasi_relawan = individu[i*2]
        alokasi_truk = individu[i*2 + 1]
        total_kekurangan += max(0, posko['kebutuhan_relawan'] - alokasi_relawan)
        total_kekurangan += max(0, posko['kebutuhan_truk'] - alokasi_truk)

    return 1 / (total_kekurangan + 1)

def seleksi(populasi_berperingkat, jumlah_elit):
    # ambil spesies unggul
    pemenang = [individu for individu, kebugaran in populasi_berperingkat[:jumlah_elit]]

    sisa = len(populasi_berperingkat) - jumlah_elit
    for _ in range(sisa):
        peserta = random.sample(populasi_berperingkat, 3)
        # PERBAIKAN: Kunci untuk max() adalah skor kebugaran itu sendiri (x[1]), bukan x[1][0]
        pemenang.append(max(peserta, key=lambda x: x[1])[0])
    return pemenang

def pindah_silang(induk1, induk2):
    posisi_potong = random.randint(1, len(induk1) - 1)
    anak = induk1[:posisi_potong] + induk2[posisi_potong:]
    return anak

def mutasi(individu, tingkat_mutasi):
    for i in range(len(individu)):
        if random.random() < tingkat_mutasi:
            # ganti ke nilai random baru
            max_val = SUMBER_DAYA['total_relawan'] if i % 2 == 0 else SUMBER_DAYA['total_truk']
            individu[i] = random.randint(0, max_val // 2) #limit
    return individu

# Visual utama web
st.title("Visualisasi Algoritma Genetika")
st.write("**Kasus:** Optimisasi Distribusi Bantuan Bencana")

# pake expander biar rapih
with st.expander("Lihat Detail Masalah"):
    st.subheader("Kebutuhan Setiap Posko")
    st.table(KEBUTUHAN_POSKO)
    st.subheader("Sumber Daya Tersedia")
    st.json(SUMBER_DAYA)

# Tombol run
if st.button("Jalankan Simulasi Evolusi"):
    with st.spinner("Komputer sedang melakukan 'evolusi'... Mohon tunggu..."):
        # inisiasi populasi
        populasi = [buat_individu() for _ in range(UKURAN_POPULASI)]
        riwayat_kebugaran = []

        # loop evolusi
        for gen in range(JUMLAH_GENERASI):
            populasi_berperingkat = sorted(
                [(individu, hitung_kebugaran(individu)) for individu in populasi],
                key=lambda x: x[1],
                reverse=True
            )

            # save skor terbaik dari generasi
            riwayat_kebugaran.append(populasi_berperingkat[0][1])

            # proses seleksi, pindah silang, dan mutasi
            induk_terpilih = seleksi(populasi_berperingkat, JUMLAH_ELIT)
            
            # 1. Bawa individu elit terbaik langsung ke generasi berikutnya
            generasi_berikutnya = [individu for individu, kebugaran in populasi_berperingkat[:JUMLAH_ELIT]]
            
            # 2. Tambah anak baru hasil dari crossover+mutasi hingga populasi penuh
            while len(generasi_berikutnya) < UKURAN_POPULASI:
                induk1, induk2 = random.sample(induk_terpilih, 2)
                anak = pindah_silang(induk1, induk2)
                generasi_berikutnya.append(mutasi(anak, TINGKAT_MUTASI))
            
    
            populasi = generasi_berikutnya

        # ambil solusi terbaik di akhir
        solusi_terbaik, skor_terbaik = sorted(
            [(individu, hitung_kebugaran(individu)) for individu in populasi],
            key=lambda x: x[1],
            reverse=True
        )[0]

    st.success("Simulasi Selesai🔥")

    # tampilkan hasil
    st.subheader("📈 Grafik Peningkatan Kebugaran per Generasi")
    st.line_chart(pd.DataFrame({
        'Generasi': range(JUMLAH_GENERASI),
        'Skor Kebugaran Terbaik': riwayat_kebugaran
    }).set_index('Generasi'))

    st.subheader("🏆 Solusi Distribusi Optimal yang Ditemukan")

    total_alokasi_relawan = 0
    total_alokasi_truk = 0

    for i, posko in enumerate(KEBUTUHAN_POSKO):
        alokasi_relawan = solusi_terbaik[i*2]
        alokasi_truk = solusi_terbaik[i*2 + 1]
        total_alokasi_relawan += alokasi_relawan
        total_alokasi_truk += alokasi_truk

        st.write(f"**{posko['nama']}**:")
        st.write(f"  - **Relawan:** {alokasi_relawan} (kebutuhan: {posko['kebutuhan_relawan']})")
        st.write(f"  - **Truk:** {alokasi_truk} (kebutuhan: {posko['kebutuhan_truk']})")

    st.info(f"**Total Alokasi:** {total_alokasi_relawan} relawan & {total_alokasi_truk} truk.")
    st.metric(label="Skor Kebugaran Final", value=f"{skor_terbaik:.4f}")
