# Dokumentasi Progress Proyek LaporKita

Dokumen ini mencatat pencapaian, status fitur, dan rencana pengembangan selanjutnya untuk sistem **LaporKita**.

---

## Status Proyek Saat Ini

Sistem **LaporKita** saat ini berada pada status **Fungsional & Siap Produksi (Production Ready)** untuk purwarupa/sistem inti. Integrasi antara database cloud, kecerdasan buatan, dan gateway notifikasi WhatsApp telah selesai dibangun dan divalidasi.

---

## Milestones & Pencapaian (Completed)

Berikut adalah detail pekerjaan yang telah diselesaikan:

### 1. Inisialisasi Lingkungan & Struktur Proyek (100% Selesai)
- [x] Merancang struktur direktori asinkronus berbasis FastAPI.
- [x] Mengonfigurasi file `requirements.txt` dengan dependensi modern (`fastapi`, `google-genai`, `sqlalchemy`, `asyncpg`, `pydantic-settings`).
- [x] Menyusun kerangka konfigurasi aman `.env` dan `.env.example` untuk melindungi kredensial API dan ID Grup WhatsApp.

### 2. Konstruksi Lapisan Basis Data Cloud (100% Selesai)
- [x] Mengintegrasikan **Supabase PostgreSQL** sebagai penyimpanan relasional utama.
- [x] Mendesain model ORM SQLAlchemy di [app/db/models.py](file:///home/superbypassudin/.clone/Github/LaporKita/app/db/models.py) (tabel `pelapor`, `laporan_mentah`, `triase_ai`).
- [x] Mengonfigurasi koneksi pooler Supabase (port 6543) dengan menonaktifkan *prepared statements* pada engine SQLAlchemy untuk kompatibilitas *Transaction Mode*.
- [x] Mengaktifkan otomatisasi pembuatan tabel pada startup aplikasi (`startup` event FastAPI).

### 3. Injeksi Mesin Logika AI (100% Selesai)
- [x] Bermigrasi ke **Google GenAI SDK** terbaru dengan menggunakan model `gemini-2.5-flash`.
- [x] Mengonfigurasi `TRIASE_SYSTEM_PROMPT` untuk klasifikasi otomatis kategori dinas, tingkat urgensi (Tinggi, Sedang, Rendah), dan penyaringan validitas lokasi.
- [x] Mengonfigurasi model AI agar secara ketat mengembalikan respons berformat JSON (`response_mime_type="application/json"`).

### 4. Integrasi WhatsApp & Webhook Disposisi (100% Selesai)
- [x] Mengganti penggunaan Meta Graph API dengan **Fonnte API** untuk mempermudah pengiriman notifikasi grup.
- [x] Mengimplementasikan pemetaan dinamis kategori dinas hasil AI ke masing-masing target ID WhatsApp Group (`WA_GROUP_*`) di file `.env`.
- [x] Menyembunyikan target Group JID sepenuhnya dari kode sumber dengan memindahkannya ke variabel lingkungan.

### 5. Orkestrasi Endpoint & Latency Bypass (100% Selesai)
- [x] Memisahkan alur kerja utama ke dalam `BackgroundTasks` FastAPI sehingga user mendapatkan respons instan (`202 Accepted`) saat mengirim formulir pengaduan.
- [x] Memproses analisis AI dan notifikasi WhatsApp di latar belakang secara asinkron.

### 6. Antarmuka Pengguna & SEO (100% Selesai)
- [x] Membuat template dasar ramah SEO dengan meta tags lengkap menggunakan Jinja2 Templates.
- [x] Merancang form keluhan publik dengan gaya minimalis, bersih, dan modern menggunakan Tailwind CSS.
- [x] Membuat skrip AJAX [app.js](file:///home/superbypassudin/.clone/Github/LaporKita/app/static/js/app.js) untuk mengirimkan data secara asinkron dan menangani status pemrosesan UI.

### 7. Uji Coba Integrasi (100% Selesai)
- [x] Membuat skrip pengujian mandiri di folder `scripts/` untuk melakukan diagnosa terisolasi:
  - [test_supabase.py](file:///home/superbypassudin/.clone/Github/LaporKita/scripts/test_supabase.py) (Lolos uji koneksi PostgreSQL & resolusi DNS).
  - [test_gemini.py](file:///home/superbypassudin/.clone/Github/LaporKita/scripts/test_gemini.py) (Lolos uji generasi konten prompt).
  - [test_fonnte.py](file:///home/superbypassudin/.clone/Github/LaporKita/scripts/test_fonnte.py) (Lolos uji pengiriman notifikasi grup).

### 8. Sistem Tiket & Pelacakan Warga (100% Selesai)
- [x] Mengenerasi kode tiket unik berformat `LK-XXXXXX` (6 karakter alfanumerik acak) untuk setiap pengaduan warga.
- [x] Membuat halaman pelacakan keluhan warga (`/lacak`) yang terintegrasi secara asinkron dengan API backend (`/api/lacak/{kode}`).
- [x] Menambahkan tombol salin kode tiket otomatis di halaman utama setelah keluhan sukses terkirim.

### 9. Dashboard Monitoring & Otentikasi Admin Sederhana (100% Selesai)
- [x] Membuat dashboard pemantauan internal (`/admin/dashboard`) yang dilindungi sesi JWT Token.
- [x] Menampilkan statistik ringkasan, visualisasi grafik jumlah laporan per dinas, dan tingkat urgensi keluhan berbasis Chart.js.
- [x] Menyederhanakan arsitektur autentikasi dengan menggunakan satu akun administrator tunggal berbasis file `.env` (`ADMIN_USERNAME` dan `ADMIN_PASSWORD`) tanpa memerlukan tabel `petugas` pada database.
- [x] Menghapus halaman registrasi petugas untuk alasan keamanan dan penyederhanaan akses.

---

## Rencana Pengembangan Selanjutnya (Next Steps)

Untuk pengembangan lebih lanjut dari sistem LaporKita, berikut adalah beberapa poin yang diusulkan:

1. **Peningkatan Akurasi Triase AI**
   - [ ] Menerapkan teknik *Few-Shot Prompting* dengan memberikan contoh aduan dan klasifikasi yang benar untuk meningkatkan akurasi analisis AI.
   - [ ] Menambahkan penanganan fallback dinas jika deskripsi keluhan tumpang tindih.
2. **Ekspor Data Laporan**
   - [ ] Menyediakan fitur ekspor daftar laporan dalam format CSV atau PDF untuk kebutuhan pelaporan dinas bulanan.

