Optimisasi Distribusi Bantuan Bencana dengan Algoritma Genetika

Deskripsi Proyek

Proyek ini adalah sebuah aplikasi web interaktif yang berfungsi sebagai alat bantu keputusan untuk mengoptimalkan distribusi sumber daya (relawan, truk, paket bantuan) ke berbagai posko saat terjadi bencana. Aplikasi ini menggunakan Algoritma Genetika untuk mencari solusi alokasi yang paling efisien dengan tujuan meminimalkan total kekurangan sumber daya. Antarmuka pengguna dibangun menggunakan Streamlit, memungkinkan pengguna untuk menyesuaikan parameter simulasi dan bahkan mengunggah dataset kebutuhan mereka sendiri secara dinamis.

Instalasi

Untuk menjalankan proyek ini di lingkungan lokal Anda, ikuti langkah-langkah berikut.

Prasyarat:
    -Python 3.9 atau versi lebih baru.
    -pip dan venv.

Langkah-langkah Instalasi:

-Clone repository ini
`git clone https://github.com/nama-anda/nama-repo-proyek.git
cd nama-repo-proyek`

Buat dan aktifkan lingkungan virtual (disarankan):
Bash

# Untuk Windows
`python -m venv venv
.\venv\Scripts\activate`

# Untuk macOS/Linux
`python3 -m venv venv
source venv/bin/activate`

Install semua paket yang dibutuhkan:
Proyek ini menggunakan beberapa library Python. Anda dapat menginstalnya dengan satu perintah menggunakan file requirements.txt.
 `   pip install -r requirements.txt`

    (Catatan: Anda perlu membuat file requirements.txt yang berisi streamlit dan pandass)

Cara Menjalankan Aplikasi

Setelah instalasi selesai, jalankan perintah berikut dari terminal di direktori utama proyek:
Bash
`
streamlit run app.py`

Aplikasi akan terbuka secara otomatis di browser default Anda. Anda dapat langsung berinteraksi dengan widget di sidebar untuk mengatur simulasi dan menekan tombol "Jalankan Simulasi Evolusi" untuk melihat hasilnya.
