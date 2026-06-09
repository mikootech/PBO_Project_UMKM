import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Pengaturan warna standar aplikasi
WARNA_PEMASUKAN = "#2E7D32"  
WARNA_PENGELUARAN = "#C62828" 
WARNA_WARUNG = "#1565C0"      
WARNA_PRIBADI = "#F57C00"    

def buat_grafik_donat_kategori(df_pengeluaran: pd.DataFrame):
    """Membuat grafik donat (pie chart berlubang) menggunakan Plotly."""
    if df_pengeluaran.empty:
        return None
        
    data_grup = df_pengeluaran.groupby('kategori')['jumlah'].sum().reset_index()
    
    fig = px.pie(
        data_grup, 
        values='jumlah', 
        names='kategori', 
        hole=0.4,
        color='kategori',
        color_discrete_map={
            'warung': WARNA_WARUNG,
            'pribadi': WARNA_PRIBADI
        }
    )
    
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    return fig

def buat_grafik_bar_bulanan(df: pd.DataFrame):
    """Membuat grafik batang perbandingan Pemasukan vs Pengeluaran per tanggal."""
    if df.empty:
        return None
        
    data_grup = df.groupby(['tanggal', 'jenis'])['jumlah'].sum().reset_index()
    
    fig = px.bar(
        data_grup,
        x='tanggal',
        y='jumlah',
        color='jenis',
        barmode='group',
        color_discrete_map={
            'pemasukan': WARNA_PEMASUKAN,
            'pengeluaran': WARNA_PENGELUARAN
        }
    )
    
    fig.update_layout(
        margin=dict(t=30, b=0, l=0, r=0),
        xaxis_title="Tanggal",
        yaxis_title="Total (Rp)",
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
    )
    return fig
