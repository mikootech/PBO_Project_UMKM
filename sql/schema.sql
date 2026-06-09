-- ============================================================
-- SCHEMA DATABASE MONEY TRACKER
-- 
-- CARA PAKAI:
-- 1. Buka Supabase Dashboard (supabase.com)
-- 2. Masuk ke project Anda
-- 3. Klik menu "SQL Editor" di kiri
-- 4. Copy-paste seluruh isi file ini
-- 5. Klik tombol "Run" / tekan Ctrl+Enter
-- ============================================================


-- ============================================================
-- TABEL 1: USERS (Pengguna Aplikasi)
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id          UUID        DEFAULT gen_random_uuid() PRIMARY KEY,
    nama        TEXT        NOT NULL,
    username    TEXT        UNIQUE NOT NULL,
    email       TEXT        UNIQUE NOT NULL,
    password_hash TEXT      NOT NULL,
    role        TEXT        DEFAULT 'user' CHECK (role IN ('admin', 'user')),
    is_active   BOOLEAN     DEFAULT TRUE,
    created_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


-- ============================================================
-- TABEL 2: TRANSACTIONS (Catatan Transaksi Keuangan)
-- ============================================================
CREATE TABLE IF NOT EXISTS transactions (
    id           UUID        DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id      UUID        REFERENCES users(id) ON DELETE CASCADE,
    jenis        TEXT        NOT NULL CHECK (jenis IN ('pemasukan', 'pengeluaran')),
    kategori     TEXT        NOT NULL CHECK (kategori IN ('kedai', 'pribadi')),
    sub_kategori TEXT        NOT NULL,
    jumlah       NUMERIC(15, 2) NOT NULL CHECK (jumlah > 0),
    catatan      TEXT        DEFAULT '',
    tanggal      DATE        NOT NULL DEFAULT CURRENT_DATE,
    created_at   TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


-- ============================================================
-- INDEX (Mempercepat pencarian data)
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_transactions_user_id  ON transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_transactions_tanggal  ON transactions(tanggal);
CREATE INDEX IF NOT EXISTS idx_transactions_jenis    ON transactions(jenis);
CREATE INDEX IF NOT EXISTS idx_transactions_kategori ON transactions(kategori);


-- ============================================================
-- MATIKAN ROW LEVEL SECURITY
-- (Agar lebih mudah untuk pemula)
-- ============================================================
ALTER TABLE users        DISABLE ROW LEVEL SECURITY;
ALTER TABLE transactions DISABLE ROW LEVEL SECURITY;


-- ============================================================
-- SELESAI!
-- 
-- Langkah selanjutnya:
-- 1. Jalankan: python setup.py
--    untuk membuat akun admin pertama
--
-- 2. Atau daftar akun baru via aplikasi,
--    lalu ubah role ke 'admin' di tabel users
-- ============================================================
