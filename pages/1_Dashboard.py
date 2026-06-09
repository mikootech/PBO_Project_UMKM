import streamlit as st
import pandas as pd
from datetime import datetime
from utils.database import get_transaksi_user
from utils.helpers import format_rupiah
from utils.charts import buat_grafik_donat_kategori, buat_grafik_bar_bulanan

if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Silakan login terlebih dahulu dari halaman utama.")
    st.stop()

st.title("🏠 Dashboard")
st.write(f"Halo, **{st.session_state.username}**! Berikut ringkasan keuanganmu.")

with st.spinner("Memuat data..."):
    data_mentah = get_transaksi_user(st.session_state.user_id)

if not data_mentah:
    st.info("Belum ada data transaksi. Silakan input di menu Transaksi.")
    st.stop()

df = pd.DataFrame(data_mentah)
df['tanggal'] = pd.to_datetime(df['tanggal'])
df['bulan_tahun'] = df['tanggal'].dt.strftime('%B %Y') 

daftar_bulan = df['bulan_tahun'].unique().tolist()
daftar_bulan.sort(reverse=True)
bulan_pilihan = st.selectbox("Pilih Bulan", daftar_bulan)
df_filter = df[df['bulan_tahun'] == bulan_pilihan].copy()

total_pemasukan = df_filter[df_filter['jenis'] == 'pemasukan']['jumlah'].sum()
total_pengeluaran = df_filter[df_filter['jenis'] == 'pengeluaran']['jumlah'].sum()
saldo = total_pemasukan - total_pengeluaran

st.markdown("### Ringkasan Bulan Ini")
warna_saldo = "text-pemasukan" if saldo >= 0 else "text-pengeluaran"
st.markdown(f"""
    <div class="saldo-box">
        <div class="saldo-title">SALDO BERSIH (BULAN INI)</div>
        <div class="saldo-amount {warna_saldo}">{format_rupiah(saldo)}</div>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.metric("Pemasukan 📈", format_rupiah(total_pemasukan))
with col2:
    st.metric("Pengeluaran 📉", format_rupiah(total_pengeluaran))

st.divider()

st.markdown("#### Aktivitas Harian")
df_grafik_bar = df_filter.copy()
df_grafik_bar['tanggal'] = df_grafik_bar['tanggal'].dt.strftime('%d %b')
fig_bar = buat_grafik_bar_bulanan(df_grafik_bar)
if fig_bar:
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

st.markdown("#### Proporsi Pengeluaran")
df_pengeluaran = df_filter[df_filter['jenis'] == 'pengeluaran']
if len(df_pengeluaran) > 0:
    fig_donat = buat_grafik_donat_kategori(df_pengeluaran)
    st.plotly_chart(fig_donat, use_container_width=True)
else:
    st.info("Belum ada pengeluaran di bulan ini.")

if len(df_pengeluaran) > 0:
    st.markdown("#### 5 Pengeluaran Terbesar")
    top_5 = df_pengeluaran.sort_values(by='jumlah', ascending=False).head(5)
    
    for _, row in top_5.iterrows():
        kategori_icon = "🏪" if row['kategori'] == "warung" else "👤"
        tgl = row['tanggal'].strftime('%d %b')
        ket = row['keterangan'] if row['keterangan'] else "Tanpa Keterangan"
        st.write(f"{kategori_icon} **{ket}** ({tgl})  \n"
                 f"<span style='color:#C62828'><b>{format_rupiah(row['jumlah'])}</b></span>", 
                 unsafe_allow_html=True)
        st.write("---")
