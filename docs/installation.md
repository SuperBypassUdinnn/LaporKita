# Panduan Instalasi LaporKita

Dokumen ini menjelaskan langkah-langkah untuk menyiapkan, mengonfigurasi, dan menjalankan aplikasi **LaporKita** pada lingkungan lokal atau server produksi.

---

## Prasyarat Sistem

Sebelum melakukan instalasi, pastikan sistem Anda telah memenuhi prasyarat berikut:

1. **Python 3.10 atau versi di atasnya** terpasang di sistem Anda.
2. **Akun Supabase** (atau server PostgreSQL lainnya) untuk menyimpan data aplikasi.
3. **Kunci API Google Gemini** dari Google AI Studio untuk modul klasifikasi otomatis (triase AI).
4. **Akun Fonnte** yang aktif beserta perangkat WhatsApp yang sudah tertaut untuk mengirimkan notifikasi.
5. **Akses internet** untuk mengunduh pustaka dependensi dan menghubungkan ke API pihak ketiga.

---

## Langkah-Langkah Instalasi

Ikuti langkah-langkah di bawah ini untuk memulai instalasi:

### 1. Kloning Repositori
Kloning repositori kode sumber LaporKita ke mesin lokal Anda menggunakan perintah berikut:
```bash
git clone https://github.com/SuperBypassUdinnn/LaporKita.git
cd LaporKita
```

### 2. Membuat Virtual Environment
Direkomendasikan untuk menggunakan lingkungan virtual (virtual environment) agar pustaka dependensi proyek tidak mengganggu lingkungan Python global Anda:
```bash
# Membuat virtual environment bernama .venv
python -m venv .venv
```

### 3. Mengaktifkan Virtual Environment
Aktifkan virtual environment sesuai dengan sistem operasi Anda:

- **Linux / macOS:**
  ```bash
  source .venv/bin/activate
  ```
- **Windows (Command Prompt):**
  ```cmd
  .venv\Scripts\activate.bat
  ```
- **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```

### 4. Mengunduh Dependensi
Setelah virtual environment aktif, pasang pustaka-pustaka yang diperlukan menggunakan pip:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Konfigurasi Lingkungan (.env)

Aplikasi menggunakan file `.env` untuk menyimpan konfigurasi sensitif seperti kredensial API dan URL database.

1. Salin contoh konfigurasi dari `.env.example`:
   ```bash
   cp .env.example .env
   ```
2. Buka file `.env` menggunakan editor teks Anda dan sesuaikan isinya sebagai berikut:

```env
# URL koneksi PostgreSQL Supabase (Menggunakan port pooler 6543)
DATABASE_URL=postgresql+asyncpg://postgres:[PASSWORD]@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres

# API Key Google Gemini
GEMINI_API_KEY=AIzaSy_KUNCI_API_GEMINI_ANDA

# Token API Fonnte
FONNTE_TOKEN=TOKEN_API_FONNTE_ANDA

# ID Grup WhatsApp Tujuan untuk Masing-masing Dinas
WA_GROUP_PU=120363xxxxxxxxx@g.us
WA_GROUP_PDAM=120363xxxxxxxxx@g.us
WA_GROUP_PERHUBUNGAN=120363xxxxxxxxx@g.us
WA_GROUP_KEBERSIHAN=120363xxxxxxxxx@g.us
WA_GROUP_SOSIAL=120363xxxxxxxxx@g.us
WA_GROUP_KESEHATAN=120363xxxxxxxxx@g.us
WA_GROUP_UMUM=120363xxxxxxxxx@g.us
```

### Catatan Penting Mengenai Database Supabase
Jika Anda menghubungkan aplikasi ke Supabase, pastikan untuk menggunakan port **6543** (Port Connection Pooler) alih-alih port standar 5432. 
Aplikasi dikonfigurasi untuk berjalan secara asinkron dengan SQLAlchemy dan `asyncpg` dalam mode transaksi pooler. Oleh karena itu, pengaturan caching prepared statements telah dimatikan di dalam kode sumber guna mencegah error bentrokan sesi koneksi database.

---

## Cara Mendapatkan ID Grup WhatsApp (JID) di Fonnte

Fonnte membutuhkan ID grup (JID) dalam format `[angka]@g.us` untuk mengirimkan notifikasi langsung ke grup koordinasi dinas terkait. Berikut cara mendapatkannya:

1. **Undang Akun Fonnte:** Undang nomor WhatsApp yang dijadikan gateway Fonnte Anda ke dalam grup koordinasi yang dituju.
2. **Kirim Perintah Informasi:** Kirim pesan `/infogroup` di grup tersebut melalui nomor lain (atau bot Fonnte). Bot Fonnte biasanya akan merespons dengan mengembalikan detail grup beserta ID Grupnya.
3. **Melalui Dashboard Fonnte:**
   - Kirim pesan biasa ke dalam grup WhatsApp tersebut.
   - Masuk ke **Dashboard Fonnte** -> buka menu **Incoming Chats** atau **Device Logs**.
   - Cari log pesan masuk terbaru yang berasal dari grup tersebut.
   - ID grup akan tertera pada data pengirim (sender), contohnya: `120363123456789@g.us`.
4. **Salin ke File .env:** Masukkan ID grup tersebut ke variabel yang sesuai dengan dinas di dalam file `.env`.

---

## Uji Coba Koneksi dan Integrasi

Sebelum menjalankan server web, disarankan untuk menguji setiap koneksi eksternal secara mandiri menggunakan skrip uji coba yang telah disediakan di folder `scripts/`:

1. **Uji Koneksi Database Supabase:**
   ```bash
   python scripts/test_supabase.py
   ```
2. **Uji Koneksi API Google Gemini:**
   ```bash
   python scripts/test_gemini.py
   ```
3. **Uji Pengiriman WhatsApp Fonnte:**
   ```bash
   python scripts/test_fonnte.py
   ```

Pastikan semua skrip di atas mengembalikan status sukses (berhasil terhubung) sebelum melanjutkan ke langkah berikutnya.

---

## Menjalankan Aplikasi

### Lingkungan Pengembangan (Development)
Untuk menjalankan server pengembangan lokal secara interaktif dengan fitur auto-reload (reload otomatis ketika kode diubah):
```bash
uvicorn app.main:app --reload
```
Aplikasi akan aktif di alamat: `http://127.0.0.1:8000`

### Pembuatan Tabel Otomatis
Aplikasi telah dilengkapi dengan pemicu otomatis untuk membuat tabel basis data (`pelapor`, `laporan_mentah`, `triase_ai`) pada saat startup pertama kali. Anda tidak perlu menjalankan skrip migrasi SQL eksternal.

### Lingkungan Produksi (Production)
Untuk deployment di lingkungan produksi, jalankan uvicorn tanpa parameter `--reload` dan sesuaikan jumlah pekerja (workers):
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```
atau menggunakan Gunicorn sebagai pengelola proses:
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```
