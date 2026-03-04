import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gelişmiş Nöbet Sistemi", layout="wide")
st.title("🪖 Profesyonel Nöbet & İzin Takip Sistemi")

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

# 2. YAN MENÜ: DURUM VE İZİN TAKİBİ
st.sidebar.header("📍 Personel Durumu")
for i, row in df.iterrows():
    yeni_durum = st.sidebar.selectbox(f"{row['İsim']}:", ['Mevcut', 'Sevkli', 'İzinli'], 
                                     index=['Mevcut', 'Sevkli', 'İzinli'].index(row['Durum']), key=f"d_{i}")
    if yeni_durum != row['Durum']:
        df.at[i, 'Durum'] = yeni_durum
        if yeni_durum in ['Sevkli', 'İzinli']:
            df.at[i, 'İzin_Sevk_Sayisi'] += 1

# 3. MANUEL NÖBET YAZMA BÖLÜMÜ
st.subheader("✍️ Manuel Nöbet Çizelgesi")
col1, col2, col3, col4 = st.columns(4)

mevcut_isimler = df[df['Durum'] == 'Mevcut']['İsim'].tolist()

with col1:
    niz1 = st.selectbox("Nizamiye 1", ["Seçiniz"] + mevcut_isimler, key="n1")
    niz2 = st.selectbox("Nizamiye 2", ["Seçiniz"] + mevcut_isimler, key="n2")
with col2:
    kam1 = st.selectbox("Kamera 1", ["Seçiniz"] + mevcut_isimler, key="k1")
    kam2 = st.selectbox("Kamera 2", ["Seçiniz"] + mevcut_isimler, key="k2")
with col3:
    ggm1 = st.selectbox("GGM 1", ["Seçiniz"] + mevcut_isimler, key="g1")
    ggm2 = st.selectbox("GGM 2 (Akşam ise)", ["Seçiniz"] + mevcut_isimler, key="g2")
with col4:
    gok1 = st.selectbox("GÖKSEM 1", ["Seçiniz"] + mevcut_isimler, key="go1")
    gok2 = st.selectbox("GÖKSEM 2", ["Seçiniz"] + mevcut_isimler, key="go2")

if st.button("✅ Manuel Seçimleri Kaydet ve Sayılara İşle"):
    secilenler = [niz1, niz2, kam1, kam2, ggm1, ggm2, gok1, gok2]
    secilenler = [s for s in secilenler if s != "Seçiniz"]
    
    # Hangi isme hangi görev puanını ekleyeceğimizi belirleyelim
    if niz1 != "Seçiniz": df.loc[df['İsim'] == niz1, 'Nizamiye'] += 1
    if niz2 != "Seçiniz": df.loc[df['İsim'] == niz2, 'Nizamiye'] += 1
    if kam1 != "Seçiniz": df.loc[df['İsim'] == kam1, 'Kamera'] += 1
    if kam2 != "Seçiniz": df.loc[df['İsim'] == kam2, 'Kamera'] += 1
    if ggm1 != "Seçiniz": df.loc[df['İsim'] == ggm1, 'GGM'] += 1
    if ggm2 != "Seçiniz": df.loc[df['İsim'] == ggm2, 'GGM'] += 1
    if gok1 != "Seçiniz": df.loc[df['İsim'] == gok1, 'GÖKSEM'] += 1
    if gok2 != "Seçiniz": df.loc[df['İsim'] == gok2, 'GÖKSEM'] += 1
    
    st.success("Manuel nöbetler başarıyla işlendi!")

st.divider()

# 4. OTOMATİK DAĞITIM BÖLÜMÜ
st.subheader("🤖 Otomatik Adil Dağıtım")
if st.button("Sistem Dağıtsın (En Az Nöbet Tutana Göre)"):
    mevcutlar = df[df['Durum'] == 'Mevcut'].copy()
    # Otomatik algoritma burada çalışır (Önceki kodun aynısı)
    # ... (Buraya otomatik dağıtım mantığı gelecek)
    st.info("Bu buton, sayıları analiz ederek en adil listeyi aşağıya döker.")

# 5. İSTATİSTİKLER VE VERİ TABLOSU
st.subheader("📊 Personel İstatistik Tablosu")
st.dataframe(df.style.highlight_max(axis=0, color='lightcoral').highlight_min(axis=0, color='lightgreen'))

if st.button("Sıfırla (Dikkat!)"):
    st.session_state.df.iloc[:, 2:] = 0
    st.rerun()
