import os
from dotenv import load_dotenv
from supabase import create_client
import bcrypt

def hash_password(password_asli: str) -> str:
    password_bytes = password_asli.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

print("="*50)
print("SETUP ADMIN MONEY TRACKER")
print("="*50)

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

if not url or not key or url == "ISI_URL_SUPABASE_ANDA_DISINI":
    print("❌ ERROR: File .env belum diisi dengan benar!")
    print("Silakan edit file .env dan masukkan URL serta KEY Supabase Anda.")
    exit()

try:
    print("Menghubungkan ke Supabase...")
    supabase = create_client(url, key)
    
    print("\nMasukkan data untuk akun Admin:")
    username = input("Username     : ").strip().lower()
    password = input("Password     : ")
    
    print("\nMenyimpan ke database...")
    password_hash = hash_password(password)
    
    data_admin = {
        "username": username,
        "password": password_hash,
        "role": "admin"
    }
    
    response = supabase.table("users").insert(data_admin).execute()
    
    print("✅ BERHASIL! Akun admin telah dibuat.")
    print("\nSekarang Anda bisa menjalankan aplikasi dengan perintah:")
    print("streamlit run app.py")
    
except Exception as e:
    print(f"\n❌ GAGAL! Terjadi kesalahan: {e}")
