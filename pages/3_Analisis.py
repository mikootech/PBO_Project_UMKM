import streamlit as st
import pandas as pd
from io import BytesIO
from utils.database import get_transaksi_user
from utils.helpers import format_rupiah

if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Silakan login terlebih dahulu dari halaman utama.")
    st.stop()

st.title("📊 Analisis Data")
st.write("Menu ini dibuat khusus menggunakan kehebatan **Pandas** untuk analisis data keuangan Anda.")

data_mentah = get_transaksi_user(st.session_state.user_id)
if not data_mentah:
    st.info("Belum ada data untuk dianalisis.")
    st.stop()

df = pd.DataFrame(data_mentah)
df['tanggal'] = pd.to_datetime(df['tanggal'])
df['bulan_tahun'] = df['tanggal'].dt.strftime('%B %Y')

level = st.selectbox("Pilih Level Analisis:", [
    "Level 1: Ringkasan Dasar (Groupby)", 
    "Level 2: Analisis Menengah (Pivot Table)",
    "Level 3: Download Excel"
])

st.divider()

if level == "Level 1: Ringkasan Dasar (Groupby)":
    st.subheader("Total per Kategori Utama")
    st.write("Mengelompokkan data berdasarkan jenis (Pemasukan/Pengeluaran) dan Kategori (Warung/Pribadi).")
    
    df_ringkasan = df.groupby(['jenis', 'kategori'])['jumlah'].sum().reset_index()
    
    for _, baris in df_ringkasan.iterrows():
        jenis = baris['jenis'].upper()
        kat = baris['kategori'].capitalize()
        angka = format_rupiah(baris['jumlah'])
        st.info(f"**{jenis} - {kat}** : {angka}")

elif level == "Level 2: Analisis Menengah (Pivot Table)":
    st.subheader("Laporan Matriks Kategori vs Bulan")
    st.write("Tabel ini menunjukkan total transaksi (Warung vs Pribadi) di setiap bulan.")
    
    df_out = df[df['jenis'] == 'pengeluaran'].copy()
    
    if df_out.empty:
        st.info("Belum ada data pengeluaran.")
    else:
        tabel_pivot = pd.pivot_table(
            df_out, 
            values='jumlah', 
            index='bulan_tahun', 
            columns='kategori', 
            aggfunc='sum',
            fill_value=0 
        )
        
        st.dataframe(tabel_pivot, use_container_width=True)
        st.caption("*Angka di atas adalah total pengeluaran.")

elif level == "Level 3: Download Excel":
    st.subheader("Export Data ke Excel")
    st.write("Download seluruh data mentah Anda ke dalam format Excel (.xlsx).")
    
    df_excel = df.copy()
    df_excel = df_excel.drop(columns=['id', 'user_id', 'created_at', 'bulan_tahun'], errors='ignore')
    
    def to_excel(df_target):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_target.to_excel(writer, index=False, sheet_name='Data_Transaksi')
        hasil_bytes = output.getvalue()
        return hasil_bytes
    
    excel_data = to_excel(df_excel)
    
    st.download_button(
        label="📥 Download Data Excel",
        data=excel_data,
        file_name='Laporan_Keuangan_MoneyTracker.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        type="primary"
    )
