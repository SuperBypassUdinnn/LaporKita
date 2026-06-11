-- Buat tabel pelapor
CREATE TABLE IF NOT EXISTS pelapor (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nik VARCHAR UNIQUE,
    nama VARCHAR,
    no_hp VARCHAR
);

-- Buat indeks untuk mempercepat pencarian berdasarkan NIK
CREATE INDEX IF NOT EXISTS idx_pelapor_nik ON pelapor(nik);

-- Buat tabel laporan_mentah
CREATE TABLE IF NOT EXISTS laporan_mentah (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pelapor_id UUID REFERENCES pelapor(id) ON DELETE CASCADE,
    kecamatan VARCHAR,
    keluhan_teks_bebas TEXT,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    kode_tiket VARCHAR UNIQUE
);

-- Buat indeks untuk mempercepat pencarian berdasarkan kode_tiket
CREATE INDEX IF NOT EXISTS idx_laporan_mentah_kode_tiket ON laporan_mentah(kode_tiket);

-- Buat tabel triase_ai
CREATE TABLE IF NOT EXISTS triase_ai (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    laporan_id UUID REFERENCES laporan_mentah(id) ON DELETE CASCADE,
    kategori_dinas VARCHAR,
    urgensi VARCHAR,
    status_json VARCHAR,
    waktu_disposisi TIMESTAMPTZ DEFAULT NOW()
);
