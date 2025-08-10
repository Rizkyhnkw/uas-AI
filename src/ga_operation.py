import random

def buat_individu(kebutuhan_list, sumber_daya_dict):
    """Membuat satu 'resep' atau solusi distribusi acak."""
    kromosom = []
    for _ in kebutuhan_list:
        alokasi_relawan = random.randint(0, sumber_daya_dict['total_relawan'])
        alokasi_truk = random.randint(0, sumber_daya_dict['total_truk'])
        alokasi_paket = random.randint(0, sumber_daya_dict['total_paket'])
        kromosom.extend([alokasi_relawan, alokasi_truk, alokasi_paket])
    return kromosom

def hitung_kebugaran(individu, kebutuhan_list, sumber_daya_dict):
    """Menilai seberapa bagus sebuah solusi dengan menghitung total kekurangan."""
    total_alokasi_relawan = sum(individu[i] for i in range(0, len(individu), 3))
    total_alokasi_truk = sum(individu[i] for i in range(1, len(individu), 3))
    total_alokasi_paket = sum(individu[i] for i in range(2, len(individu), 3))

     # tunda jika alokasi > sumberdaya
    if (total_alokasi_relawan > sumber_daya_dict['total_relawan'] or
        total_alokasi_truk > sumber_daya_dict['total_truk'] or
        total_alokasi_paket > sumber_daya_dict['total_paket']):
        return 0

    #hitung total kekurangan
    total_kekurangan = 0
    for i, posko in enumerate(kebutuhan_list):
        alokasi_relawan = individu[i*3]
        alokasi_truk = individu[i*3 + 1]
        alokasi_paket = individu[i*3 + 2]
        total_kekurangan += max(0, posko['kebutuhan_relawan'] - alokasi_relawan)
        total_kekurangan += max(0, posko['kebutuhan_truk'] - alokasi_truk)
        total_kekurangan += max(0, posko['kebutuhan_paket'] - alokasi_paket)
        
    return 1 / (total_kekurangan + 1)

def seleksi(populasi_berperingkat, jumlah_elit):
    """Memilih individu terbaik untuk menjadi 'induk' generasi berikutnya."""
    pemenang = [individu for individu, kebugaran in populasi_berperingkat[:jumlah_elit]]
    sisa = len(populasi_berperingkat) - jumlah_elit
    for _ in range(sisa):
        peserta = random.sample(populasi_berperingkat, 3)
        pemenang.append(max(peserta, key=lambda x: x[1])[0])
    return pemenang

def pindah_silang(induk1, induk2):
    """Mengkombinasikan 'DNA' dari dua induk untuk menciptakan 'anak'."""
    posisi_potong = random.randint(1, len(induk1) - 1)
    anak = induk1[:posisi_potong] + induk2[posisi_potong:]
    return anak

def mutasi(individu, tingkat_mutasi, sumber_daya_dict):
    """Memberi perubahan kecil acak pada 'DNA' untuk variasi."""
    for i in range(len(individu)):
        if random.random() < tingkat_mutasi:
            if i % 3 == 0:
                max_val = sumber_daya_dict['total_relawan']
            elif i % 3 == 1:
                max_val = sumber_daya_dict['total_truk']
            else:
                max_val = sumber_daya_dict['total_paket']
            individu[i] = random.randint(0, max_val // 2)
    return individu

def jalankan_evolusi(kebutuhan_posko, sumber_daya, ukuran_populasi, jumlah_generasi, tingkat_mutasi, jumlah_elit, progress_callback=None):
    """Fungsi utama yang menjalankan seluruh siklus evolusi."""
    populasi = [buat_individu(kebutuhan_posko, sumber_daya) for _ in range(ukuran_populasi)]
    riwayat_kebugaran = []

    for gen in range(jumlah_generasi):
        populasi_berperingkat = sorted(
            [(ind, hitung_kebugaran(ind, kebutuhan_posko, sumber_daya)) for ind in populasi],
            key=lambda x: x[1],
            reverse=True
        )
        
        riwayat_kebugaran.append(populasi_berperingkat[0][1])
        
        if progress_callback:
            progress_callback(gen + 1, jumlah_generasi, riwayat_kebugaran)

        induk_terpilih = seleksi(populasi_berperingkat, jumlah_elit)
        
        generasi_berikutnya = [ind for ind, keb in populasi_berperingkat[:jumlah_elit]]
        
        while len(generasi_berikutnya) < ukuran_populasi:
            induk1, induk2 = random.sample(induk_terpilih, 2)
            anak = pindah_silang(induk1, induk2)
            generasi_berikutnya.append(mutasi(anak, tingkat_mutasi, sumber_daya))
        
        populasi = generasi_berikutnya
        
    # ambil solusi terbaik di akhir
    solusi_terbaik, skor_terbaik = sorted(
        [(ind, hitung_kebugaran(ind, kebutuhan_posko, sumber_daya)) for ind in populasi],
        key=lambda x: x[1],
        reverse=True
    )[0]

    return solusi_terbaik, skor_terbaik, riwayat_kebugaran
