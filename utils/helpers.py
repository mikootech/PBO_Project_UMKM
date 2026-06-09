def format_rupiah(angka):
    """Mengubah angka biasa menjadi format Rupiah yang mudah dibaca.
    Contoh: 1500000 -> 'Rp 1.500.000'
    """
    try:
        angka = int(angka)
        teks = f"Rp {angka:,.0f}".replace(",", ".")
        return teks
    except:
        return "Rp 0"
