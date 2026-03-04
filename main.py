import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gelişmiş Nöbet Sistemi", layout="wide")
st.title("🪖 Akıllı Nöbet & İzin Takip Sistemi")

# 1. HAFIZA YÖNETİMİ
if 'df' not in st.session_state:
    isimler = [
        "Mustafa YILDIZ", "Mehmet KÜÇÜK", "Rahman KAVCIOĞLU", "Mustafa BAL", 
        "Mehmet DÜĞEROĞLU", "Ogün KARAKAYA", "Mert ÇEKER", "Uğur ERDOĞAN", 
        "Ekrem DEMİR", "Hüseyin HANEFİO", "Murat YILMAZER", 
        "İbrahim Burak GÖRÜCÜ", "Ahmet ASLAN", "Muhammed Seyit DİRİCANLI", "Furkan ÇELİK"
    ]
    st.session_state.df = pd.DataFrame({
        'İsim': isimler,
        'Durum': ['Mevcut'] * len(isimler),
        'Nizamiye': [0]*len(isimler), 'Kamera': [0]*len(isimler), 
        'GGM': [0]*len(isimler), 'GÖKSEM': [0]*len(isimler), 
        'Yaya_Devriye': [0]*len(isimler), 'İzin_Sevk_Sayisi': [0]*len(isimler)
    })

df = st.session_state.df

# 2. YAN MENÜ: DURUM GÜNCELLEME
st.sidebar.header("📍 Personel Durumu")
for i, row in df.iterrows():
    yeni_durum = st.sidebar.selectbox(f"{row['İsim']}:", ['Mevcut', 'Sevkli', 'İzinli'], 
                                     index=['Mevcut', 'Sevkli', 'İzinli'].index(row['Durum']), key=f"d_{i}")
    df.at[i, 'Durum'] = yeni_durum

# 3. MANUEL GÖREV YAZMA (BİRBİRİNİ ENGELLEYEN SEÇİMLER)
st.subheader("✍️ Manuel Görev Çizelgesi")
st.info("Bir listede seçtiğiniz isim, diğer listelerden otomatik olarak çıkarılır.")

# Mevcut olanları filtrele
mevcut_isimler = df[df['Durum'] == 'Mevcut']['İsim'].tolist()
secilen_isimler = []

def akilli_liste(mevcutlar, secilenler):
    return [isim for isim in mevcutlar if isim not in secilenler]

col1, col2, col3, col4 = st.columns(4)

with col1:
    niz1 = st.selectbox("Nizamiye 1", ["Seçiniz"] + akilli_liste(mevcut_isimler, secilen_isimler), key="n1")
    if niz1 != "Seçiniz": secilen_isimler.append(niz1)
    niz2 = st.selectbox("Nizamiye 2", ["Seçiniz"] + akilli_liste(mevcut_isimler, secilen_isimler), key="n2")
    if niz2 != "Seçiniz": secilen_isimler.append(niz2)

with col2:
    kam1 = st.selectbox("Kamera 1", ["Seçiniz"] + akilli_liste(mevcut_isimler, secilen_isimler), key="k1")
    if kam1 != "Seçiniz": secilen_isimler.append(kam1)
    kam2 = st.selectbox("Kamera 2", ["Seçiniz"] + akilli_liste(mevcut_isimler, secilen_isimler), key="k2")
    if kam2 != "Seçiniz": secilen_isimler.append(kam2)

with col3:
    ggm1 = st.selectbox("GGM 1", ["Seçiniz"] + akilli_liste(mevcut_isimler, secilen_isimler), key="g1")
    if ggm1 != "Seçiniz": secilen_isimler.append(ggm1)
    ggm2 = st.selectbox("GGM 2", ["Seçiniz"] + akilli_liste(mevcut_isimler, secilen_isimler), key="g2")
    if ggm2 != "Seçiniz": secilen_isimler.append(ggm2)

with col4:
    gok1 = st.selectbox("GÖKSEM 1", ["Seçiniz"] + akilli_liste(mevcut_isimler, secilen_isimler), key="go1")
    if gok1 != "Seçiniz": secilen_isimler.append(gok1)
    gok2 = st.selectbox("GÖKSEM 2", ["Seçiniz"] + akilli_liste(mevcut_isimler, secilen_isimler), key="go2")
    if gok2 != "Seçiniz": secilen_isimler.append(gok2)

# İZİN VE SEVKLİLER İÇİN MANUEL SAYI EKLEME
st.divider()
st.subheader("📋 Manuel İzin / Sevk Sayısı Ekle")
izinli_sevkli_isimler = df[df['Durum'] != 'Mevcut']['İsim'].tolist()
manuel_izin_secim = st.multiselect("Bugün İzin/Sevk hanesine +1 eklenecekleri seçin:", izinli_sevkli_isimler)

if st.button("🚀 Tüm Seçimleri Kaydet ve Sayılara İşle"):
    # Nöbetleri işle
    if niz1 != "Seçiniz": df.loc[df['İsim'] == niz1, 'Nizamiye'] += 1
    if niz2 != "Seçiniz": df.loc[df['İsim'] == niz2, 'Nizamiye'] += 1
    if kam1 != "Seçiniz": df.loc[df['İsim'] == kam1, 'Kamera'] += 1
    if kam2 != "Seçiniz": df.loc[df['İsim'] == kam2, 'Kamera'] += 1
    if ggm1 != "Seçiniz": df.loc[df['İsim'] == ggm1, 'GGM'] += 1
    if ggm2 != "Seçiniz": df.loc[df['İsim'] == ggm2, 'GGM'] += 1
    if gok1 != "Seçiniz": df.loc[df['İsim'] == gok1, 'GÖKSEM'] += 1
    if gok2 != "Seçiniz": df.loc[df['İsim'] == gok2, 'GÖKSEM'] += 1
    
    # İzinleri işle
    for isim in manuel_izin_secim:
        df.loc[df['İsim'] == isim, 'İzin_Sevk_Sayisi'] += 1
    
    st.success("Tüm veriler başarıyla güncellendi!")
    st.rerun()

st.divider()

# 4. İSTATİSTİKLER VE VERİ TABLOSU
st.subheader("📊 Personel İstatistik Tablosu")
st.dataframe(df.style.highlight_max(axis=0, color='lightcoral').highlight_min(axis=0, color='lightgreen'))

if st.button("⚠️ Tüm Sayacı Sıfırla"):
    st.session_state.df.iloc[:, 2:] = 0
    st.rerun()
