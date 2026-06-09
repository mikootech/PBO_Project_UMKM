import streamlit as st
import pandas as pd
from utils.database import get_semua_user, get_semua_transaksi
from utils.helpers import format_rupiah

if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Silakan login terlebih dahulu.")
    st.stop()

if st.session_state.role != 'admin':
    st.error("Akses Ditolak! Halaman ini khusus untuk Administrator.")
    st.stop()

st.title("🔐 Panel Admin")
st.write("Selamat datang, Admin! Di sini Anda bisa melihat seluruh data aplikasi.")

tab_users, tab_global = st.tabs(["👥 Kelola Pengguna", "🌐 Statistik Global"])

with tab_users:
    st.subheader("Daftar Pengguna Aplikasi")
    
    with st.spinner("Memuat data pengguna..."):
        users_data = get_semua_user()
        
    if not users_data:
        st.info("Belum ada user yang terdaftar.")
    else:
        df_users = pd.DataFrame(users_data)
        st.dataframe(df_users, use_container_width=True)
        st.caption("Total Pengguna: " + str(len(df_users)))

with tab_global:
    st.subheader("Ringkasan Seluruh Transaksi")
    st.write("Data di bawah adalah gabungan transaksi dari SEMUA user.")
    
    with st.spinner("Memuat seluruh transaksi..."):
        all_trx = get_semua_transaksi()
        
    if not all_trx:
        st.info("Belum ada transaksi di dalam sistem.")
    else:
        df_all = pd.DataFrame(all_trx)
        
        total_in = df_all[df_all['jenis'] == 'pemasukan']['jumlah'].sum()
        total_out = df_all[df_all['jenis'] == 'pengeluaran']['jumlah'].sum()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Perputaran Uang Masuk", format_rupiah(total_in))
        with col2:
            st.metric("Total Perputaran Uang Keluar", format_rupiah(total_out))
            
        st.divider()
        
        st.write("**Total Transaksi per Kategori (Global)**")
        df_global_group = df_all.groupby('kategori')['jumlah'].sum().reset_index()
        
        for _, row in df_global_group.iterrows():
            st.write(f"- {row['kategori'].capitalize()}: **{format_rupiah(row['jumlah'])}**")
