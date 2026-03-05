import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gelişmiş Nöbet Sistemi", layout="wide")
st.title("🪖 Akıllı Nöbet, Durum ve Hastane Takip Sistemi")

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
        'Nizamiye': [0]*len(isimler), 'Kamera': [0]*len(isimler), 
        'GGM': [0]*len(isimler), 'GÖKSEM': [0]*len(isimler), 
        'İstirahat_Sayisi': [0]*len(isimler), 
        'Sevk_Sayisi': [0]*len(isimler)
    })

df = st.session_state.df

# 2. SEÇİM MANTIĞI VE FİLTRELEME
st.subheader("✍️ Günlük Görev ve Durum Belirleme")
secilen_toplam = []

def kalan_isimler(hepsi, secilenler):
    return [isim for isim in hepsi if isim not in secilenler]

# --- MANUEL GÖREVLER ---
st.write("### 🛡️ Nöbet Yerleri")
col1, col2, col3, col4 = st.columns(4)
with col1:
    n1 = st.selectbox("Nizamiye 1", ["Seçiniz"] + kalan_isimler(df['İsim'].tolist(), secilen_toplam), key="n1")
    if n1 != "Seçiniz": secilen_toplam.append(n1)
    n2 = st.selectbox("Nizamiye 2", ["Seçiniz"] + kalan_isimler(df['İsim'].tolist(), secilen_toplam), key="n2")
    if n2 != "Seçiniz": secilen_toplam.append(n2)
with col2:
    k1 = st.selectbox("Kamera 1", ["Seçiniz"] + kalan_isimler(df['İsim'].tolist(), secilen_toplam), key="k1")
    if k1 != "Seçiniz": secilen_toplam.append(k1)
    k2 = st.selectbox("Kamera 2", ["Seçiniz"] + kalan_isimler(df['İsim'].tolist(), secilen_toplam), key="k2")
    if k2 != "Seçiniz": secilen_toplam.append(k2)
with col3:
    g1 = st.selectbox("GGM 1", ["Seçiniz"] + kalan_isimler(df['İsim'].tolist(), secilen_toplam), key="g1")
    if g1 != "Seçiniz": secilen_toplam.append(g1)
    g2 = st.selectbox("GGM 2", ["Seçiniz"] + kalan_isimler(df['İsim'].tolist(), secilen_toplam), key="g2")
    if g2 != "Seçiniz": secilen_toplam.append(g2)
with col4:
    go1 = st.selectbox("GÖKSEM 1", ["Seçiniz"] + kalan_isimler(df['İsim'].tolist(), secilen_toplam), key="go1")
    if go1 != "Seçiniz": secilen_toplam.append(go1)
    go2 = st.selectbox("GÖKSEM 2", ["Seçiniz"] + kalan_isimler(df['İsim'].tolist(), secilen_toplam), key="go2")
    if go2 != "Seçiniz": secilen_toplam.append(go2)

st.divider()

# --- DURUM VE HASTANE BÖLÜMÜ ---
c_ist, c_sevk, c_hast = st.columns(3)
with c_ist:
    st.write("🏥 **İstirahatliler**")
    ist_sec = st.multiselect("İstirahatli seç:", kalan_isimler(df['İsim'].tolist(), secilen_toplam), key="ist")
    secilen_toplam.extend(ist_sec)

with c_sevk:
    st.write("🚑 **Sevkliler**")
    sevk_sec = st.multiselect("Sevkli seç:", kalan_isimler(df['İsim'].tolist(), secilen_toplam), key="sevk")
    secilen_toplam.extend(sevk_sec)

with c_hast:
    st.write("🏥 **Hastane Personeli**")
    hast_sec = st.multiselect("Hastaneye gidenleri seç:", kalan_isimler(df['İsim'].tolist(), secilen_toplam), key="hast")
    secilen_toplam.extend(hast_sec)

# --- KAYDETME BUTONU ---
st.divider()
if st.button("💾 Tüm Çizelgeyi Kay
