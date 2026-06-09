import bcrypt

def hash_password(password_asli: str) -> str:
    """Mengubah password biasa menjadi kode acak (hash) untuk keamanan."""
    # Convert string ke bytes
    password_bytes = password_asli.encode('utf-8')
    # Buat salt (pengacak tambahan)
    salt = bcrypt.gensalt()
    # Buat hash
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def cek_password(password_asli: str, password_hash: str) -> bool:
    """Mengecek apakah password yang dimasukkan cocok dengan hash di database."""
    # Convert string ke bytes
    password_bytes = password_asli.encode('utf-8')
    hash_bytes = password_hash.encode('utf-8')
    
    # Cek kecocokan
    return bcrypt.checkpw(password_bytes, hash_bytes)
