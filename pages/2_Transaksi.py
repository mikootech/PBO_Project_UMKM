import streamlit as st
import pandas as pd
from datetime import date
from utils.database import tambah_transaksi, get_transaksi_user, hapus_transaksi
from utils.helpers import format_rupiah

if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Silakan login terlebih dahulu dari halaman utama.")
    st.stop()

st.title("📝 Transaksi")

tab_input, tab_riwayat = st.tabs(["➕ Input Baru", "📋 Riwayat"])

with tab_input:
    st.write("Catat pemasukan atau pengeluaran baru di sini.")
    
    with st.form("form_transaksi"):
        col1, col2 = st.columns(2)
        with col1:
            jenis = st.selectbox("Jenis", ["Pengeluaran", "Pemasukan"])
        with col2:
            kategori = st.selectbox("Kategori", ["Warung", "Pribadi"])
            
        tanggal = st.date_input("Tanggal", value=date.today())
        jumlah = st.number_input("Nominal (Rp)", min_value=0, step=1000)
        keterangan = st.text_input("Keterangan Tambahan")
        
        submit = st.form_submit_button("Simpan Transaksi", type="primary")
        
        if submit:
            if jumlah <= 0:
                st.error("Nominal tidak boleh 0!")
            else:
                jenis_db = jenis.lower()
                kategori_db = kategori.lower()
                
                hasil = tambah_transaksi(
                    user_id=st.session_state.user_id,
                    jenis=jenis_db,
                    kategori=kategori_db,
                    keterangan=keterangan,
                    jumlah=jumlah,
                    tanggal=tanggal
                )
                
                if hasil is not None:
                    st.success("✅ Transaksi berhasil disimpan!")
                    st.balloons()
                else:
                    st.error("❌ Gagal menyimpan transaksi.")

with tab_riwayat:
    st.write("10 Transaksi Terakhir Anda")
    
    data_mentah = get_transaksi_user(st.session_state.user_id)
    
    if not data_mentah:
        st.info("Belum ada transaksi yang dicatat.")
    else:
        df = pd.DataFrame(data_mentah)
        df = df.sort_values(by=['tanggal', 'created_at'], ascending=[False, False])
        df_top10 = df.head(10)
        
        for index, row in df_top10.iterrows():
            with st.container(border=True): 
                c1, c2 = st.columns([2, 1])
                with c1:
                    icon_jenis = "📉" if row['jenis'] == 'pengeluaran' else "📈"
                    ket = row['keterangan'] if row['keterangan'] else "Tanpa keterangan"
                    st.write(f"{icon_jenis} **{ket}**")
                    st.caption(f"{row['tanggal']} | {row['kategori'].capitalize()}")
                with c2:
                    warna = "#C62828" if row['jenis'] == 'pengeluaran' else "#2E7D32"
                    st.write(f"<span style='color:{warna}; font-weight:bold; font-size:14px;'>{format_rupiah(row['jumlah'])}</span>", unsafe_allow_html=True)
                
                if st.button(f"Hapus", key=f"btn_hapus_{row['id']}", help="Hapus transaksi ini"):
                    hapus_transaksi(row['id'])
                    st.success("Dihapus! Silakan refresh (tarik layar ke bawah / tekan R).")
                    st.rerun()
