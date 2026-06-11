# LaporKita - Sistem Otomatisasi Triase Keluhan Publik

LaporKita adalah platform inovatif berbasis FastAPI untuk mengotomatisasi manajemen pengaduan masyarakat. Menggunakan teknologi kecerdasan buatan (AI) dari Google Gemini, sistem ini secara pintar menganalisis konten keluhan, mengelompokkannya ke dinas terkait, menentukan tingkat urgensi, serta mengirimkan notifikasi instan via WhatsApp Group dinas melalui Fonnte.

---

## Fitur Utama & Pembaruan

### 1. Peningkatan Akurasi Triase AI (Few-Shot Prompting & Fallback)
* **Few-Shot Prompting**: Menggunakan teknik penyusunan prompt terstruktur dengan memberikan beberapa pasang contoh input-output konkret untuk memandu AI menghasilkan keputusan klasifikasi dinas, tingkat urgensi, dan status validitas (`ACCEPTED` / `REJECTED`) yang jauh lebih konsisten.
* **Penanganan Fallback**: Logika khusus di dalam prompt untuk menangani keluhan kompleks dengan deskripsi masalah yang saling tumpang tindih (multi-kategori), yang secara otomatis akan mengarahkannya ke dinas infrastruktur utama dengan tingkat urgensi penanganan tertinggi.
* **Response Mime Type**: Memaksa model `gemini-1.5-flash` mengembalikan output dalam format JSON murni (`application/json`) demi menjamin kelancaran proses parsing data ke database.

### 2. Sistem Tiket & Pelacakan Warga
* **Kode Tiket Unik**: Setiap laporan yang berhasil disimpan ke sistem akan secara otomatis mendapatkan kode pelacakan acak sepanjang 8 karakter alphanumeric dengan format `LK-XXXXXX`.
* **Pelacakan Real-time Publik**: Menyediakan form pencarian tiket pada halaman beranda utama. Warga dapat memasukkan kode tiket mereka untuk memantau status disposisi AI (`status_json`), dinas yang dituju, tingkat urgensi, serta status progress penanganan (`status_proses`) dari pihak dinas terkait.
* **Payload Notifikasi Terintegrasi**: Kode tiket ini juga disisipkan langsung ke dalam skema background task untuk dikirimkan melalui WhatsApp Group dinas agar petugas dapat melakukan rujukan balik dengan mudah.

### 3. Otentikasi Petugas Dinas (JWT Authentication)
* **JSON Web Token (JWT)**: Mengamankan endpoint internal sistem menggunakan enkripsi token `HS256`. Petugas dinas harus melakukan otentikasi terlebih dahulu untuk memperoleh token akses yang valid selama 8 jam.
* **Secure Route**: Menyediakan gerbang endpoint `/auth/login` berbasis form data untuk memverifikasi kredensial petugas sebelum mereka diberikan izin mengelola dashboard internal.

### 4. Dashboard Monitoring Internal (Backoffice API)
* **Endpoint Statistik Konten**: Menyediakan rute `/admin/dashboard-stats` yang mengembalikan metrik akumulasi data agregat secara asinkron dari basis data, mencakup:
  * Total seluruh laporan yang masuk ke dalam sistem.
  * Akumulasi laporan yang lolos verifikasi AI (`ACCEPTED`).
  * Akumulasi keluhan yang ditolak otomatis oleh AI (`REJECTED`) karena terdeteksi sebagai pesan junk/tidak jelas.

---

## Struktur Direktori Utama

```text
LaporKita/
├── app/
│   ├── api/
│   │   └── routes.py          # Definisi endpoint (Home, Submit, Track, Auth, Stats)
│   ├── core/
│   │   └── config.py          # Pengaturan aplikasi & Pemetaan grup WhatsApp Fonnte
│   ├── db/
│   │   ├── database.py        # Konfigurasi session basis data asinkron SQLAlchemy
│   │   └── models.py          # Model tabel basis data (Pelapor, LaporanMentah, TriaseAI)
│   ├── services/
│   │   ├── llm_service.py     # Integrasi Google GenAI SDK dengan Few-Shot Prompting
│   │   └── wa_service.py      # Integrasi pengiriman notifikasi gateway Fonnte
│   ├── static/
│   │   └── js/
│   │       └── app.js         # Logika AJAX frontend (Submit laporan & Pelacakan tiket)
│   ├── templates/
│   │   ├── base.html          # Template induk layout dengan Tailwind CSS
│   │   └── index.html         # Tampilan beranda utama (Form Laporan & Form Lacak)
│   ├── schemas.py             # Validasi payload data masukan menggunakan Pydantic
│   └── tasks.py               # Logika pemrosesan background task (AI & WA)
├── .env                       # File konfigurasi sensitif (API Key, Database URL, Token)
├── main.py                    # Entry point utama aplikasi FastAPI
└── README.md                  # Dokumentasi teknis proyek