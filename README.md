# LaporKita - Sistem Otomatisasi Triase Keluhan Publik

[Laporan Tugas Akhir Sistem Informasi C](https://docs.google.com/document/d/15LISFFhB2P2YJeu6NCEfySJRpqHzojJAFwou4GGsTY8/edit?tab=t.43tkkdk70h6c)

**LaporKita** adalah platform pengaduan masyarakat pintar berbasis web yang dirancang untuk mempercepat proses penanganan laporan warga. Dengan memanfaatkan kecerdasan buatan (**Google Gemini 2.5 Flash**), sistem ini secara otomatis mengklasifikasikan kategori dinas, menentukan tingkat urgensi, memvalidasi kelengkapan informasi spasial/lokasi aduan, serta meneruskan notifikasi secara langsung ke grup WhatsApp dinas terkait melalui **Fonnte API**.

---

## Tujuan Pengembangan Aplikasi

Aplikasi **LaporKita** dikembangkan dengan tujuan untuk:
1. **Mempercepat Pelayanan Publik:** Mengotomatisasi proses triase laporan masyarakat secara instan tanpa memerlukan petugas manual untuk memilah jenis keluhan.
2. **Efisiensi Disposisi:** Meneruskan keluhan langsung ke kelompok kerja/dinas yang berwenang via grup WhatsApp secara otomatis.
3. **Mengurangi Sampah Informasi:** Menyaring pengaduan yang tidak valid (misal: aduan spam atau yang tidak mencantumkan lokasi kejadian yang jelas) secara otomatis menggunakan AI.
4. **Meningkatkan Transparansi:** Memberikan kemudahan bagi masyarakat untuk melacak status penanganan aduan secara real-time menggunakan kode tiket.

---

## Fitur Utama

- **AI-Powered Triaging (Zero-Shot Classification):** Menggunakan **Gemini 2.5 Flash** untuk menganalisis teks keluhan bebas dari warga secara instan.
- **Validasi Spasial Otomatis:** Laporan yang tidak menyertakan lokasi kejadian yang jelas (nama jalan, bangunan, atau kecamatan) akan otomatis ditolak (`REJECTED`) oleh AI guna menyaring aduan spam atau aduan tidak lengkap.
- **WhatsApp Group Routing:** Pesan keluhan diteruskan langsung ke grup WhatsApp dinas terkait (Dinas PU, Dinas PDAM, Dinas Perhubungan, Dinas Kebersihan, Dinas Sosial, Dinas Kesehatan, Dinas Umum) secara dinamis menggunakan **Fonnte API**.
- **Sistem Tiket & Pelacakan Keluhan Warga:** Menghasilkan kode tiket unik `LK-XXXXXX` (6 karakter alfanumerik acak) untuk setiap keluhan yang berhasil dikirim. Warga dapat memantau status disposisi dinas dan tingkat urgensi secara real-time melalui halaman `/lacak`.
- **Dashboard Pemantauan & Statistik Internal Admin (Backoffice):** Halaman `/admin/dashboard` yang menampilkan ringkasan statistik aduan (Total Laporan, Laporan Ditolak, Persentase Diterima) dan grafik visual distribusi laporan per dinas/urgensi menggunakan Chart.js.
- **Sesi Keamanan Admin Terproteksi:** Autentikasi portal admin berbasis JWT token yang disimpan dengan aman dalam cookie HTTPOnly. Menggunakan akun administrator tunggal terpusat via kredensial `.env` tanpa pendaftaran petugas mandiri di database.
- **Bypass Latensi dengan Background Tasks:** Menggunakan fitur `BackgroundTasks` dari FastAPI untuk menyimpan laporan mentah terlebih dahulu, kemudian memproses triase AI dan pengiriman WhatsApp di latar belakang. Klien web mendapatkan respons instan (`HTTP 202 Accepted`) tanpa menunggu panggilan API eksternal selesai.
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
- **Visualisasi & Charting:** Chart.js v4 (Daftar Laporan, Distribusi Urgensi, Laporan per Dinas)

---

## Struktur Database

Aplikasi menggunakan database relasional PostgreSQL dengan tiga tabel utama berikut:

### 1. Tabel `pelapor`
Menyimpan informasi identitas unik warga yang melakukan pelaporan aduan.
| Nama Kolom | Tipe Data | Atribut | Deskripsi |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | ID unik pelapor |
| `nik` | VARCHAR | UNIQUE, INDEX | NIK pelapor (16 digit) |
| `nama` | VARCHAR | NOT NULL | Nama lengkap pelapor |
| `no_hp` | VARCHAR | NOT NULL | Nomor HP / WhatsApp pelapor |

### 2. Tabel `laporan_mentah`
Menyimpan isi data laporan mentah yang diinputkan oleh warga.
| Nama Kolom | Tipe Data | Atribut | Deskripsi |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | ID unik laporan |
| `pelapor_id` | UUID | FOREIGN KEY REFERENCES `pelapor(id)` | Referensi ke pelapor |
| `kecamatan` | VARCHAR | NOT NULL | Lokasi kecamatan kejadian |
| `keluhan_teks_bebas` | TEXT | NOT NULL | Deskripsi keluhan warga |
| `timestamp` | TIMESTAMPTZ| DEFAULT NOW() | Waktu laporan diterima |
| `kode_tiket` | VARCHAR | UNIQUE, INDEX | Kode tiket alfanumerik (`LK-XXXXXX`) |

### 3. Tabel `triase_ai`
Menyimpan hasil klasifikasi cerdas AI (Gemini) dan status penanganan/disposisi laporan.
| Nama Kolom | Tipe Data | Atribut | Deskripsi |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | ID unik triase |
| `laporan_id` | UUID | FOREIGN KEY REFERENCES `laporan_mentah(id)` | Referensi ke laporan |
| `kategori_dinas` | VARCHAR | NOT NULL | Klasifikasi dinas penerima |
| `urgensi` | VARCHAR | NOT NULL | Tingkat urgensi aduan (`Tinggi`, `Sedang`, `Rendah`) |
| `status_json` | VARCHAR | NOT NULL | Status aduan (`ACCEPTED`, `REJECTED`) |
| `waktu_disposisi` | TIMESTAMPTZ| DEFAULT NOW() | Waktu disposisi notifikasi |

---

## Screenshot Tampilan Aplikasi

Berikut adalah dokumentasi visual antarmuka sistem **LaporKita**:

### 1. Form Pengaduan Warga
Halaman utama di mana masyarakat dapat mengirim laporan dengan mengisi identitas diri dan keluhan secara bebas.
![Form Keluhan Publik](assets/img/form-keluhan.png)

### 2. Halaman Lacak Status Keluhan
Halaman pelacakan keluhan warga dengan memasukkan kode tiket untuk memantau status disposisi dinas dan tingkat urgensi secara real-time.
![Cek Status Keluhan](assets/img/form-cek-status-keluhan.png)

### 3. Dashboard Pemantauan Admin (Backoffice)
Halaman dashboard monitoring internal dinas yang menyajikan ringkasan statistik aduan dan diagram distribusi laporan per dinas/urgensi menggunakan Chart.js.
![Dashboard Admin](assets/img/admin-dashboard.png)

### 4. Detail Modal Keluhan & Riwayat
Tampilan modal rincian pengaduan yang memuat detail identitas pelapor (Nama, NIK, No. HP) secara lengkap bagi petugas admin yang terautentikasi.
![Detail Keluhan](assets/img/riwayat-keluhan.png)

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

# Kredensial Administrator Portal Dinas (Hardcoded)
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
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