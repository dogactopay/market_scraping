# Function for adjusting sub category names. (Meyve(42)==>Meyve and integer value 42)
def qua_str(k):
    k = k.replace('(', '')
    k = k.replace(')', '')
    k = int(k)
    return k


def fiyat_duzenle(veri):
    veri = veri.replace('.', '')
    veri = veri.replace(',', '.')
    veri = veri.replace(' TL', '')
    veri = float(veri)

    return veri
