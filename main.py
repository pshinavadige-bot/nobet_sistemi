import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gelişmiş Nöbet Sistemi", layout="wide")
st.title("🪖 Akıllı Nöbet & Durum Takip Sistemi")

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
        'Yaya_Devriye': [0]*len(isimler), 
        'İstirahat_Sayisi': [0]*len(isimler), 
        'Sevk_Sayisi': [0]*len(isimler)
    })

df = st.session_state.df

# 2. SEÇİM MANTIĞI (BİRBİRİNİ ENGELLEYEN LİSTELER)
st.subheader("✍️ Günlük Görev ve Durum Çizelgesi")
st.info("Bir bölümde seçilen isim diğer bölümlerde listelenmez.")

secilen_toplam = []

def kalan_isimler(hepsi, secilenler):
    return [isim for isim in hepsi if isim not in secilenler]

# --- GÖREV BÖLÜMÜ ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    n1 = st.selectbox("Nizamiye 1", ["Seçiniz"] + kalan_isimler(df['İsim'].tolist(), secilen_toplam))
    if n1 != "Seçiniz": secilen_toplam.append(n1)
    n2 = st.selectbox("Nizamiye 2", ["Seçiniz"] + kalan_isimler(df['İsim'].tolist(), secilen_toplam))
    if n2 != "Seçiniz": secilen_toplam.append(n2)
with col2:
    k1 = st.selectbox("Kamera 1", ["Seçiniz"] + kalan_isimler(df['İsim'].tolist(), secilen_toplam))
    if k1 != "Seçiniz": secilen_toplam.append(k1)
    k2 = st.selectbox("Kamera 2", ["Seçiniz"] + kalan_isimler(df['İsim'].tolist(), secilen_toplam))
    if k2 != "Seçiniz": secilen_toplam.append(k2)
with col3:
    g1 = st.selectbox("GGM 1", ["Seçiniz"] + kalan_isimler(df['İsim'].tolist(), secilen_toplam))
    if g1 != "Seçiniz": secilen_toplam.append(g1)
    g2 = st.selectbox("GGM 2", ["Seçiniz"] + kalan_isimler(df['İsim'].tolist(), secilen_toplam))
    if g2 != "Seçiniz": secilen_toplam.append(g2)
with col4:
    go1 = st.selectbox("GÖKSEM 1", ["Seçiniz"] + kalan_isimler(df['İsim'].tolist(), secilen_toplam))
    if go1 != "Seçiniz": secilen_toplam.append(go1)
    go2 = st.selectbox("GÖKSEM 2", ["Seçiniz"] + kalan_isimler(df['İsim'].tolist(), secilen_toplam))
    if go2 != "Seçiniz": secilen_toplam.append(go2)

st.divider()

# --- İSTİRAHAT VE SEVK BÖLÜMÜ ---
c_ist, c_sevk = st.columns(2)
with c_ist:
    st.write("🏥 **İstirahatliler**")
    istirahatli_secilenler = st.multiselect("Bugün istirahatli olanları seçin:", 
                                            kalan_isimler(df['İsim'].tolist(), secilen_toplam))
    secilen_toplam.extend(istirahatli_secilenler)

with c_sevk:
    st.write("🚑 **Sevkliler**")
    sevkli_secilenler = st.multiselect("Bugün sevkli olanları seçin:", 
                                       kalan_isimler(df['İsim'].tolist(), secilen_toplam))
    secilen_toplam.extend(sevkli_secilenler)

# --- KAYDETME BUTONU ---
if st.button("💾 Tüm Çizelgeyi Kaydet ve Sayıları Güncelle"):
    # Nöbetleri işle
    if n1 != "Seçiniz": df.loc[df['İsim'] == n1, 'Nizamiye'] += 1
    if n2 != "Seçiniz": df.loc[df['İsim'] == n2, 'Nizamiye'] += 1
    if k1 != "Seçiniz": df.loc[df['İsim'] == k1, 'Kamera'] += 1
    if k2 != "Seçiniz": df.loc[df['İsim'] == k2, 'Kamera'] += 1
    if g1 != "Seçiniz": df.loc[df['İsim'] == g1, 'GGM'] += 1
    if g2 != "Seçiniz": df.loc[df['İsim'] == g2, 'GGM'] += 1
    if go1 != "Seçiniz": df.loc[df['İsim'] == go1, 'GÖKSEM'] += 1
    if go2 != "Seçiniz": df.loc[df['İsim'] == go2, 'GÖKSEM'] += 1
    
    # İstirahat ve Sevkleri işle
    for isim in istirahatli_secilenler:
        df.loc[df['İsim'] == isim, 'İstirahat_Sayisi'] += 1
    for isim in sevkli_secilenler:
        df.loc[df['İsim'] == isim, 'Sevk_Sayisi'] += 1
        
    st.success("Veriler başarıyla işlendi ve sayaçlar güncellendi!")
    st.rerun()

st.divider()

# 4. İSTATİSTİK TABLOSU
st.subheader("📊 Personel Görev ve Durum İstatistikleri")
st.dataframe(df.style.highlight_max(axis=0, color='lightcoral').highlight_min(axis=0, color='lightgreen'))

if st.button("⚠️ Tüm Verileri Sıfırla"):
    st.session_state.df.iloc[:, 1:] = 0
    st.rerun()
