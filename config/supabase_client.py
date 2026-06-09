import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load variabel dari file .env
load_dotenv()

# Mengambil URL dan Key dari .env
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

# Buat fungsi untuk mendapatkan koneksi supabase
def get_supabase() -> Client:
    # Cek apakah URL dan Key sudah diisi
    if not url or not key or url == "ISI_URL_SUPABASE_ANDA_DISINI":
        raise ValueError("Supabase URL atau Key belum disetting di file .env!")
    
    return create_client(url, key)
