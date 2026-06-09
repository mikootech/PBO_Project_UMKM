import streamlit as st
from config.supabase_client import get_supabase
from utils.auth import hash_password, cek_password

st.set_page_config(
    page_title="Money Tracker",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

def load_css():
    try:
        with open("assets/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass 

load_css()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'role' not in st.session_state:
    st.session_state.role = None

def main():
    if st.session_state.logged_in:
        st.success(f"Selamat datang, {st.session_state.username}! 👋")
        st.info("Silakan buka menu di sebelah kiri 👈 untuk mulai menggunakan aplikasi.")
        
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.role = None
            st.rerun()
        return

    st.title("💰 Money Tracker")
    st.write("Catat keuangan Warung dan Pribadi Anda dengan mudah dari HP.")
    
    tab_login, tab_daftar = st.tabs(["🔑 Login", "📝 Daftar Baru"])
    
    # --- TAB LOGIN ---
    with tab_login:
        st.subheader("Masuk ke Akun Anda")
        
        with st.form("form_login"):
            username = st.text_input("Username").strip().lower()
            password = st.text_input("Password", type="password")
            submit_login = st.form_submit_button("Masuk", type="primary")
            
            if submit_login:
                if not username or not password:
                    st.error("Username dan password harus diisi!")
                else:
                    try:
                        supabase = get_supabase()
                        response = supabase.table("users").select("*").eq("username", username).execute()
                        users = response.data
                        
                        if len(users) == 0:
                            st.error("Username tidak ditemukan!")
                        else:
                            user_data = users[0]
                            # Cek password menggunakan bcrypt hash
                            if cek_password(password, user_data['password']):
                                st.session_state.logged_in = True
                                st.session_state.user_id = user_data['id']
                                st.session_state.username = user_data['username']
                                st.session_state.role = user_data['role']
                                st.success("Login berhasil!")
                                st.rerun() 
                            else:
                                st.error("Password salah!")
                    except Exception as e:
                        st.error(f"Gagal koneksi ke database: {e}")

    # --- TAB DAFTAR BARU ---
    with tab_daftar:
        st.subheader("Buat Akun Baru")
        
        with st.form("form_daftar"):
            new_username = st.text_input("Username (tanpa spasi)").strip().lower()
            new_password = st.text_input("Password", type="password")
            new_password_confirm = st.text_input("Konfirmasi Password", type="password")
            
            submit_daftar = st.form_submit_button("Daftar Sekarang", type="primary")
            
            if submit_daftar:
                if not new_username or not new_password:
                    st.warning("Semua kolom harus diisi!")
                elif ' ' in new_username:
                    st.warning("Username tidak boleh pakai spasi!")
                elif new_password != new_password_confirm:
                    st.warning("Password tidak cocok!")
                elif len(new_password) < 6:
                    st.warning("Password minimal 6 karakter!")
                else:
                    try:
                        supabase = get_supabase()
                        cek_user = supabase.table("users").select("id").eq("username", new_username).execute()
                        if len(cek_user.data) > 0:
                            st.error("Username sudah terpakai, silakan pilih yang lain.")
                        else:
                            password_hash = hash_password(new_password)
                            data_baru = {
                                "username": new_username,
                                "password": password_hash,
                                "role": "user" 
                            }
                            supabase.table("users").insert(data_baru).execute()
                            st.success("Pendaftaran berhasil! Silakan Login di tab sebelah.")
                    except Exception as e:
                        st.error(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    main()
