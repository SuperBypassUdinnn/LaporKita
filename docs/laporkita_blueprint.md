# Rencana Implementasi Sistem LaporKita

Dokumen ini merupakan cetak biru teknis untuk merekayasa dan mengimplementasikan sistem otomatisasi triase keluhan publik **LaporKita**. Arsitektur dibangun menggunakan kerangka kerja asinkronus dengan pemisahan lapisan (Separation of Concerns) untuk mengintegrasikan antarmuka ramah SEO, basis data relasional, mesin logika kecerdasan buatan, dan webhook notifikasi.

## Tumpukan Teknologi (Tech Stack)
* **Backend:** Python 3.10+, FastAPI, Uvicorn
* **Database & ORM:** SQLite (Purwarupa awal), SQLAlchemy
* **AI Middleware:** Google Generative AI (Gemini 1.5 Flash)
* **Notifikasi:** Meta Graph API (WhatsApp)
* **Frontend:** HTML5, TailwindCSS (CDN), Vanilla JS, Jinja2 Templates (SSR untuk SEO)

---

## FASE 1: Inisialisasi Lingkungan dan Dependensi
Fokus pada tahap ini adalah mengisolasi lingkungan pengembangan dan memastikan seluruh pustaka fundamental tersedia.

### 1. Struktur Direktori Proyek ✅

### 2. Konfigurasi requirements.txt ✅

### 3. Konfigurasi .env
Cuplikan isi:
```.env
DATABASE_URL=sqlite:///./laporkita.db
GEMINI_API_KEY=AIzaSy_YOUR_GEMINI_KEY_HERE
WA_ACCESS_TOKEN=EAAB_YOUR_META_TOKEN_HERE
WA_PHONE_NUMBER_ID=YOUR_WA_PHONE_ID
```

---

## FASE 2: Konstruksi Lapisan Basis Data (SQLAlchemy)
Membangun skema relasional tabel untuk menampung aliran data mentah dan hasil ekstraksi kecerdasan buatan.

### 1. Inisialisasi Mesin Database (app/db/database.py)
- Impor create_engine, sessionmaker, dan declarative_base dari SQLAlchemy.
- Buat engine yang merujuk pada DATABASE_URL dari file konfigurasi.
- Konfigurasikan sesi SessionLocal untuk membuka jalur transaksi ke database.

### 2. Definisi Skema Tabel (app/db/models.py)
Deklarasikan tiga entitas tabel utama:
- Pelapor: Menyimpan data identitas entitas pengguna (ID, Nama, NIK, No. HP).
- LaporanMentah: Menyimpan log asli (ID, ID_Pelapor, Kecamatan, Keluhan_Teks_Bebas, Timestamp).
- TriaseAI: Tabel relasional yang menyimpan hasil JSON dari LLM (ID, ID_Laporan, Kategori_Dinas, Urgensi, Status_JSON, Waktu_Disposisi).

---

## FASE 3: Injeksi Mesin Logika (Gemini AI & WhatsApp)
Membangun modul independen untuk menangani panggilan API pihak ketiga guna mencegah spaghetti code.

### 1. Rekayasa Prompt (app/core/prompts.py)
- Susun variabel string TRIASE_SYSTEM_PROMPT.
- Tulis instruksi Zero-Shot Classification ketat yang memaksa Gemini memformat balasan murni sebagai JSON: {"kategori_dinas": "...", "urgensi": "...", "status": "..."} dan aturan validasi jika teks warga tidak memiliki lokasi jalan yang jelas.

### 2. Layanan Pemrosesan LLM (app/services/llm_service.py)
- Lakukan inisialisasi kunci API via google.generativeai.configure().
- Buat fungsi asinkronus process_triage(text: str) yang mengkombinasikan teks warga dengan TRIASE_SYSTEM_PROMPT.
- Fungsi harus mencakup error handling (try-except) jika respons JSON dari AI gagal di-parsing.

### 3. Layanan Disposisi Webhook (app/services/wa_service.py)
- Buat fungsi asinkronus send_wa_notification(payload: dict).
- Gunakan pustaka httpx.AsyncClient untuk melakukan HTTP POST ke Endpoint Meta Graph API.
- Susun template pesan dinamis yang memasukkan data dinas, lokasi keluhan, dan tingkat urgensi.

---

## FASE 4: Orkestrasi Endpoint & Background Tasks
Menyusun titik akses lalu lintas data di FastAPI dengan mengamankan latensi menggunakan penugasan latar belakang (BackgroundTasks).

### 1. Pembuatan Routes (app/api/routes.py)
- GET /: Merender template HTML Jinja2 (Landing Page & Form).
- POST /submit-laporan: Endpoint utama untuk menerima payload dari antarmuka web menggunakan python-multipart.

### 2. Implementasi Eksekusi Asinkronus (Bypass Latensi)
Di dalam endpoint POST /submit-laporan:
- Simpan data masukan warga langsung ke tabel LaporanMentah via SQLAlchemy.
- Injeksi fungsi pemrosesan ke background: background_tasks.add_task(run_triage_and_notify, laporan_id, teks_keluhan).
- Kembalikan respons HTTP 202 (Accepted) seketika ke klien web.

---

## FASE 5: Rendering Antarmuka Ramah SEO (Jinja2)
Membangun presentasi frontend berbasis Server-Side Rendering (SSR) murni agar mesin pencari dapat mengindeks konten.

### 1. Kerangka Dasar (app/templates/base.html)
- Susun struktur HTML5.
- Injeksi atribut meta wajib (Title, Description, Keywords, Open Graph) untuk kepatuhan SEO.
- Masukkan integrasi CDN TailwindCSS.

### 2. Halaman Interaksi (app/templates/index.html)
- Kembangkan form yang terdiri dari: <select> terstruktur untuk input entitas Kecamatan/Kelurahan dan <textarea> untuk menampung teks bebas keluhan.

### 3. Skrip Klien (app/static/js/app.js)
- Tangkap event listener pada tombol submit.
- Gunakan fungsi e.preventDefault() untuk mencegah reload browser.
- Eksekusi fetch() API untuk POST data ke /submit-laporan dan tampilkan indikator interaktif (misal: "Laporan sedang diproses AI") kepada pengguna.

---

## FASE 6: Pengujian dan Validasi (Manual Testing oleh Manusia)
Lakukan uji fungsi sistem secara end-to-end melalui eksekusi lokal:
uvicorn app.main:app --reload
## Skenario Pengujian Mutlak:
1. Uji Valid (Positive Test):
- Input: "Pipa air bersih PDAM bocor parah dan membanjiri jalan utama di depan minimarket, mohon segera ditangani."
- Ekspektasi: Baris log mencetak ekstraksi JSON (Dinas PDAM, Urgensi Tinggi), database ter-update, dan webhook sukses mengirim pesan WhatsApp ke device tujuan.

2. Uji Halusinasi/Informasi Kurang (Negative Test):
- Input: "Gimana sih ini kok gelap banget gak ada lampu, tolong kerja dong." (Tanpa lokasi spasial).
- Ekspektasi: LLM mengembalikan atribut JSON {"status": "REJECTED"}, sistem basis data menolak disposisi, dan webhook WhatsApp memblokir pengiriman (bypass digagalkan) agar tim lapangan tidak menerima informasi sampah.