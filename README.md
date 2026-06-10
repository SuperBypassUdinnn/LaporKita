# LaporKita - Sistem Otomatisasi Triase Keluhan Publik

**LaporKita** adalah platform pengaduan masyarakat pintar berbasis web yang dirancang untuk mempercepat proses penanganan laporan warga. Dengan memanfaatkan kecerdasan buatan (**Google Gemini 2.5 Flash**), sistem ini secara otomatis mengklasifikasikan kategori dinas, menentukan tingkat urgensi, memvalidasi kelengkapan informasi spasial/lokasi aduan, serta meneruskan notifikasi secara langsung ke grup WhatsApp dinas terkait melalui **Fonnte API**.

---

## Fitur Utama

- **AI-Powered Triaging (Zero-Shot Classification):** Menggunakan **Gemini 2.5 Flash** untuk menganalisis teks keluhan bebas dari warga secara instan.
- **Validasi Spasial Otomatis:** Laporan yang tidak menyertakan lokasi kejadian yang jelas (nama jalan, bangunan, atau kecamatan) akan otomatis ditolak (`REJECTED`) oleh AI guna menyaring laporan spam.
- **WhatsApp Group Routing:** Pesan keluhan tidak dikirim ke nomor pribadi, melainkan langsung ke **WhatsApp Group** instan yang sesuai dengan kategori dinas (misal: Dinas PU, Dinas PDAM, Dinas Kebersihan, dll.) menggunakan **Fonnte API**.
- **Bypass Latensi dengan Background Tasks:** Menggunakan fitur `BackgroundTasks` dari FastAPI untuk menyimpan laporan mentah terlebih dahulu, kemudian memproses triase AI dan pengiriman WhatsApp di latar belakang. Klien web mendapatkan respons instan (`HTTP 202 Accepted`) tanpa perlu menunggu panggilan API eksternal selesai.
- **Supabase Integration & Connection Pooling:** Menggunakan database relasional PostgreSQL di cloud Supabase secara asinkron dengan SQLAlchemy dan `asyncpg`. Dikonfigurasi secara khusus untuk menonaktifkan *prepared statements* agar kompatibel dengan *Transaction Mode* pada pooler Supabase (port 6543).
- **SEO-Optimized SSR Frontend:** Menggunakan Server-Side Rendering (SSR) berbasis Jinja2 Templates dengan penataan visual menggunakan Tailwind CSS yang responsif, modern, dan ramah terhadap mesin pencari (SEO-Friendly).

---

## Tumpukan Teknologi (Tech Stack)

- **Backend Framework:** FastAPI (Python 3.10+)
- **Server:** Uvicorn
- **Database & ORM:** Supabase PostgreSQL & SQLAlchemy (Async Session) + asyncpg
- **AI Middleware:** Google GenAI SDK (Gemini 2.5 Flash)
- **WhatsApp Gateway:** Fonnte API
- **Frontend:** HTML5, Tailwind CSS (via CDN), Vanilla JS, & Jinja2 Templates

---

## Struktur Direktori

```text
LaporKita/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py             # Route endpoints (form rendering & submission)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py             # Konfigurasi Pydantic Settings
│   │   └── prompts.py            # Prompt rekayasa triase AI
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py           # Inisialisasi engine asyncpg & session
│   │   └── models.py             # Definisi skema tabel (Pelapor, Laporan, Triase)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm_service.py        # Integrasi Google GenAI SDK (Gemini)
│   │   └── wa_service.py         # Integrasi Fonnte API (WhatsApp)
│   ├── static/
│   │   └── js/
│   │       └── app.js            # Interaksi asinkronus frontend form submit
│   ├── templates/
│   │   ├── base.html             # Base layout HTML & SEO meta tags
│   │   └── index.html            # Halaman utama & form keluhan publik
│   ├── main.py                   # Titik masuk aplikasi & auto-migration
│   ├── schemas.py                # Skema Pydantic untuk data validation & AI output
│   └── tasks.py                  # Background tasks untuk triase & notifikasi
├── docs/
│   ├── architecture.md           # Arsitektur sistem (frontend & backend)
│   ├── installation.md           # Panduan instalasi dan konfigurasi
│   ├── laporkita_blueprint.md    # Dokumen cetak biru rekayasa sistem
│   └── progress.md               # Dokumentasi progress & rencana pengembangan
├── scripts/
│   ├── test_fonnte.py            # Skrip tes pengiriman WhatsApp Fonnte
│   ├── test_gemini.py            # Skrip tes koneksi Gemini API
│   └── test_supabase.py          # Skrip tes koneksi Supabase & DNS
├── .env.example                  # Contoh konfigurasi environment variables
├── requirements.txt              # Daftar dependensi Python
└── README.md                     # Panduan penggunaan proyek (Dokumen ini)
```

---

## Instalasi & Konfigurasi

### 1. Prasyarat
Sebelum memulai, pastikan Anda memiliki:
- Python 3.10 atau lebih baru terpasang di sistem.
- Akun Supabase (untuk mendapatkan URL koneksi PostgreSQL).
- API Key Google Gemini (didapatkan dari Google AI Studio).
- Akun Fonnte dengan kuota pesan aktif dan nomor WhatsApp yang telah ditautkan.

### 2. Kloning Repository & Setup Virtual Environment
```bash
git clone https://github.com/SuperBypassUdinnn/LaporKita.git
cd LaporKita

# Membuat virtual environment
python -m venv .venv

# Mengaktifkan virtual environment (Linux/macOS)
source .venv/bin/activate

# Mengaktifkan virtual environment (Windows)
# .venv\Scripts\activate
```

### 3. Mengunduh Dependensi
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Konfigurasi Environment Variables (`.env`)
Salin file `.env.example` menjadi `.env`:
```bash
cp .env.example .env
```
Buka file `.env` yang baru dibuat dan isi variabel berikut:
```env
# Koneksi Database Supabase (Port 6543 untuk Transaction Pooler)
DATABASE_URL=postgresql+asyncpg://postgres:[PASSWORD]@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres

# API Key Google Gemini
GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxxxxxx

# Fonnte API Token
FONNTE_TOKEN=your_fonnte_token_here

# WhatsApp Group JID (Group ID) untuk Masing-masing Dinas
WA_GROUP_PU=120363xxxxxxxxx@g.us
WA_GROUP_PDAM=120363xxxxxxxxx@g.us
WA_GROUP_PERHUBUNGAN=120363xxxxxxxxx@g.us
WA_GROUP_KEBERSIHAN=120363xxxxxxxxx@g.us
WA_GROUP_SOSIAL=120363xxxxxxxxx@g.us
WA_GROUP_KESEHATAN=120363xxxxxxxxx@g.us
WA_GROUP_UMUM=120363xxxxxxxxx@g.us
```

> [!IMPORTANT]
> - Gunakan port **6543** di `DATABASE_URL` untuk menggunakan Transaction Pooler Supabase.
> - Aplikasi dikonfigurasi dengan menonaktifkan *prepared statement cache* untuk menghindari konflik sesi pada Supabase Transaction Mode.

---

## Cara Mendapatkan WhatsApp Group ID (JID) di Fonnte

Untuk mengarahkan pesan dinamis ke grup WhatsApp tertentu, Anda membutuhkan ID Group (JID) tujuan yang berformat `120363xxxxxxxxxx@g.us`. Berikut langkah-langkah untuk mendapatkannya:

1. **Undang Nomor Fonnte ke dalam Grup:**
   Masukkan nomor WhatsApp yang Anda daftarkan di perangkat Fonnte Anda ke dalam grup dinas yang telah dibuat.
2. **Kirim Perintah `/infogroup`:**
   Kirimkan pesan bertuliskan `/infogroup` di dalam grup tersebut melalui nomor lain (atau nomor Fonnte jika didukung). Sistem bot Fonnte biasanya akan secara otomatis membalas dengan menampilkan informasi grup beserta ID-nya.
3. **Menggunakan Fitur Logs/Webhook di Dashboard Fonnte:**
   - Kirim pesan biasa apa saja ke dalam grup.
   - Buka **Dashboard Fonnte** -> masuk ke menu **Incoming Chats** atau **Device Logs**.
   - Cari baris chat baru yang masuk dari grup tersebut.
   - Salin ID grup yang muncul pada kolom pengirim, biasanya berakhiran `@g.us` (contoh: `120363123456789@g.us`).
4. **Masukkan ke file `.env`:**
   Tempelkan ID Group tersebut ke variabel lingkungan yang sesuai (misal: `WA_GROUP_PU`, `WA_GROUP_PDAM`, dsb.).

---

## Skrip Pengujian

Sebelum menjalankan aplikasi secara penuh, Anda dapat memverifikasi masing-masing integrasi pihak ketiga secara mandiri menggunakan skrip di dalam folder `scripts/`:

```bash
# 1. Menguji koneksi database Supabase & verifikasi DNS
python scripts/test_supabase.py

# 2. Menguji koneksi & respons AI Google Gemini (gemini-2.5-flash)
python scripts/test_gemini.py

# 3. Menguji pengiriman pesan WhatsApp Fonnte ke grup
python scripts/test_fonnte.py
```

---

## Menjalankan Aplikasi

Jalankan server pengembangan lokal dengan perintah berikut:

```bash
uvicorn app.main:app --reload
```

- Server akan aktif dan dapat diakses melalui browser di alamat: `http://127.0.0.1:8000`
- **Migrasi Database:** Saat aplikasi pertama kali dijalankan (peristiwa *startup*), SQLAlchemy secara otomatis akan membuat tabel-tabel (`pelapor`, `laporan_mentah`, `triase_ai`) di Supabase jika belum ada.