# MRI Survey System - BPS Provinsi Lampung

Aplikasi berbasis web yang dibangun menggunakan **Streamlit** untuk melakukan survei kepribadian MRI (*Motivation, Relation, Impact*) bagi pegawai BPS Provinsi Lampung. Sistem ini menganalisis respons pengguna untuk menentukan aspek kepribadian dominan dan area yang perlu dikembangkan, serta menyediakan dashboard analitik untuk administrator.

## 🌟 Fitur Utama

### 👤 User Mode (Peserta)
*   **Autentikasi Valid:** Login menggunakan Username BPS dan NIP yang divalidasi terhadap database (`biodata.csv`).
*   **Pemilihan Satker:** Mendukung pemilihan Satuan Kerja di lingkungan BPS Provinsi Lampung.
*   **Survei Interaktif:**
    *   60 pertanyaan yang diacak secara dinamis.
    *   Mekanisme pemilihan 3 pernyataan yang paling sesuai dari 6 opsi.
    *   Progress bar real-time.
*   **Hasil Instan:**
    *   Visualisasi **Top 10 Aspek Dominan**.
    *   Visualisasi **5 Aspek untuk Pengembangan**.
    *   Penjelasan detail arti setiap aspek dan dimensinya.

### 🔐 Admin Mode (Dashboard)
*   **Login Aman:** Proteksi password untuk akses dashboard.
*   **Dashboard Analitik:**
    *   Statistik total peserta dan waktu survei terakhir.
    *   Ranking rata-rata skor aspek secara global.
    *   Analisis frekuensi aspek populer (Top 10 & Bottom 5).
    *   Analisis distribusi dimensi (*Motivation, Relation, Impact*).
*   **Analisis Satker:** Profil karakteristik kepribadian spesifik per Satuan Kerja.
*   **Manajemen Data:**
    *   Tabel data lengkap peserta.
    *   Fitur pencarian status pengerjaan berdasarkan username.
    *   Ekspor data hasil survei ke format CSV.

## 🛠️ Teknologi yang Digunakan

*   **Python 3.x**
*   **Streamlit:** Framework antarmuka web.
*   **Pandas:** Manipulasi dan analisis data.
*   **Plotly:** Visualisasi data interaktif (Bar chart, Pie chart, Box plot).

## 📂 Struktur Folder

Pastikan struktur folder proyek Anda disusun seperti berikut agar aplikasi dapat membaca aset data dengan benar:

```text
mri/
├── app.py                  # File utama aplikasi (Source code)
├── survey_results.csv      # File output hasil survei (Dibuat otomatis oleh sistem)
├── README.md               # Dokumentasi proyek
└── assets/
    └── data/
        ├── biodata.csv     # Database pegawai (Kolom: username_bps, nama, nip)
        └── data_mri.csv    # Bank soal (Kolom: Dimensi, Aspek, Arti, Perilaku Kuat, Perilaku Lemah)
```

## 🚀 Cara Menjalankan Aplikasi

1.  **Persiapan Lingkungan:**
    Pastikan Python sudah terinstal. Install library yang dibutuhkan melalui terminal:
    ```bash
    pip install streamlit pandas plotly
    ```

2.  **Persiapan Data:**
    Pastikan file `assets/data/biodata.csv` dan `assets/data/data_mri.csv` sudah tersedia di direktori yang sesuai.

3.  **Jalankan Aplikasi:**
    Buka terminal di direktori proyek (`c:\Users\asus\python\mri\`) dan jalankan perintah:
    ```bash
    streamlit run app.py
    ```

4.  **Akses Aplikasi:**
    Aplikasi akan terbuka otomatis di browser default Anda (biasanya di `http://localhost:8501`).

## 🔑 Informasi Kredensial

*   **Password Admin Default:** `admin123`
    *(Dapat diubah pada variabel `ADMIN_PASSWORD` di dalam file `app.py`)*

## 📝 Catatan Teknis

*   **Penyimpanan Data:** Hasil survei disimpan secara lokal di file `survey_results.csv`. Jika file belum ada, aplikasi akan membuatnya secara otomatis saat ada data masuk.
*   **Validasi:** Sistem melakukan pengecekan *case-insensitive* untuk username dan memastikan NIP hanya berupa angka.
*   **Session State:** Aplikasi menggunakan `st.session_state` untuk menjaga data progres survei agar tidak hilang saat terjadi interaksi ulang (rerun) pada halaman.

---
© 2024 MRI Survey System
