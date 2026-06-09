from config.supabase_client import get_supabase
import pandas as pd

def get_transaksi_user(user_id: int):
    """Mengambil semua transaksi milik satu user tertentu."""
    supabase = get_supabase()
    response = supabase.table("transaksi").select("*").eq("user_id", user_id).execute()
    return response.data

def tambah_transaksi(user_id: int, jenis: str, kategori: str, keterangan: str, jumlah: float, tanggal: str):
    """Menambahkan data transaksi baru ke database."""
    supabase = get_supabase()
    data_baru = {
        "user_id": user_id,
        "jenis": jenis,
        "kategori": kategori,
        "jumlah": jumlah,
        "keterangan": keterangan,
        "tanggal": str(tanggal)
    }
    response = supabase.table("transaksi").insert(data_baru).execute()
    return response.data

def hapus_transaksi(transaksi_id: int):
    """Menghapus transaksi berdasarkan ID."""
    supabase = get_supabase()
    response = supabase.table("transaksi").delete().eq("id", transaksi_id).execute()
    return response.data

def get_semua_user():
    """Mengambil semua data user (hanya untuk Admin)."""
    supabase = get_supabase()
    response = supabase.table("users").select("id, username, role").execute()
    return response.data

def get_semua_transaksi():
    """Mengambil semua data transaksi dari semua user (hanya untuk Admin)."""
    supabase = get_supabase()
    response = supabase.table("transaksi").select("*").execute()
    return response.data
