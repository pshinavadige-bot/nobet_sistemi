import streamlit as st
import pandas as pd

st.set_page_config(page_title="Basit Nöbet Sistemi", layout="wide")
st.title("🪖 Manuel Nöbet ve Durum Çizelgesi")

# 1. PERSONEL LİSTESİ
isim_listesi = [
    "Mustafa YILDIZ", "Mehmet KÜÇÜK", "Rahman KAVCIOĞLU", "Mustafa BAL", 
    "Mehmet DÜĞEROĞLU", "Ogün KARAKAYA", "Mert ÇEKER", "Uğur ERDOĞAN", 
    "Ekrem DEMİR", "Hüseyin HANEFİO", "Murat YILMAZER", 
    "İbrahim Burak GÖRÜCÜ", "Ahmet ASLAN", "Muhammed Seyit DİRİCANLI", "Furkan ÇELİK"
]

# 2. HAFIZA SİSTEMİ
if 'veri' not in st.session_state:
    st.session_state.veri = pd.DataFrame({
        'İsim': isim_listesi,
        'Nizamiye': 0, 'Kamera': 0, 'GGM': 0, 'GÖKSEM': 0,
        'İstirahat': 0, 'Sevk': 0
    })

df = st.session_state.veri

# 3. GÜNLÜK SEÇİMLER
st.subheader("📋 Bugünün Görevlilerini Seç")
c1, c2, c3, c4 = st.columns(4)

with c1:
    n1 = st.selectbox("Nizamiye 1", ["-"] + isim_listesi)
    n2 = st.selectbox("Nizamiye 2", ["-"] + isim_listesi)
with c2:
    k1 = st.selectbox("Kamera 1", ["-"] + isim_listesi)
    k2 = st.selectbox("Kamera 2", ["-"] + isim_listesi)
with c3:
    g1 = st.selectbox("GGM 1", ["-"] + isim_listesi)
    g2 = st.selectbox("GGM 2", ["-"] + isim_listesi)
with c4:
    go1 = st.selectbox("GÖKSEM 1", ["-"] + isim_listesi)
    go2 = st.selectbox("GÖKSEM 2", ["-"] + isim_listesi)

st.divider()
st.subheader("🏥 Durum Takibi (Çoklu Seçim)")
col_ist, col_sevk, col_hast = st.columns(3)

with col_ist:
    secilen_ist = st.multiselect("İstirahatliler (+1)", isim_listesi)
with col_sevk:
    secilen_sevk = st.multiselect("Sevkliler (+1)", isim_listesi)
with col_hast:
    secilen_hast = st.multiselect("Hastane Görevi (Sayılmaz)", isim_listesi)

# 4. KAYDETME
if st.button("💾 VERİLERİ KAYDET VE SAYILARI ARTIR"):
    # Nöbetleri ekle (Her if'in altındaki satır 1 TAB içerde olmalı)
    if n1 != "-":
        df.loc[df['İsim'] == n1, 'Nizamiye'] += 1
    if n2 != "-":
        df.loc[df['İsim'] == n2, 'Nizamiye'] += 1
    if k1 != "-":
        df.loc[df['İsim'] == k1, 'Kamera'] += 1
    if k2 != "-":
        df.loc[df['İsim'] == k2, 'Kamera'] += 1
    if g1 != "-":
        df.loc[df['İsim'] == g1, 'GGM'] += 1
    if g2 != "-":
        df.loc[df['İsim'] == g2, 'GGM'] += 1
    if go1 != "-":
        df.loc[df['İsim'] == go1, 'GÖKSEM'] += 1
    if go2 != "-":
        df.loc[df['İsim'] == go2, 'GÖKSEM'] += 1
    
    # Durumları ekle
    for isim in secilen_ist:
        df.loc[df['İsim'] == isim, 'İstirahat'] += 1
    for isim in secilen_sevk:
        df.loc[df['İsim'] == isim, 'Sevk'] += 1
    
    st.success("Başarıyla kaydedildi!")
    st.rerun()

st.divider()

# 5. GENEL TABLO
st.subheader("📊 Toplam Nöbet ve Durum Sayıları")
st.dataframe(df)

if st.button("⚠️ Tüm Sayacı Sıfırla"):
    st.session_state.veri.iloc[:, 1:] = 0
    st.rerun()
