import streamlit as st
import pandas as pd

# Uygulama Başlığı
st.set_page_config(page_title="Nöbet Dağıtım Sistemi", layout="wide")
st.title("🪖 Bölük Nöbet & Görev Takip Sistemi")

# 1. BÖLÜM: PERSONEL LİSTESİ TANIMLAMA
if 'personel_df' not in st.session_state:
    isimler = [
        "Mustafa YILDIZ", "Mehmet KÜÇÜK", "Rahman KAVCIOĞLU", "Mustafa BAL", 
        "Mehmet DÜĞEROĞLU", "Ogün KARAKAYA", "Mert ÇEKER", "Uğur ERDOĞAN", 
        "Ekrem DEMİR", "Hüseyin HANEFİO", "Murat YILMAZER", 
        "İbrahim Burak GÖRÜCÜ", "Ahmet ASLAN", "Muhammed Seyit DİRİCANLI", "Furkan ÇELİK"
    ]
    data = {
        'İsim': isimler,
        'Durum': ['Mevcut'] * len(isimler),
        'Nizamiye': [0] * len(isimler),
        'Kamera': [0] * len(isimler),
        'GGM': [0] * len(isimler),
        'GÖKSEM': [0] * len(isimler),
        'Yaya_Devriye': [0] * len(isimler)
    }
    st.session_state.personel_df = pd.DataFrame(data)

df = st.session_state.personel_df

# 2. BÖLÜM: DURUM GÜNCELLEME (SEVKLİLER)
st.sidebar.header("Personel Durum Yönetimi")
st.sidebar.info("Sevkli veya izinli olanları buradan işaretle.")

for i, row in df.iterrows():
    df.at[i, 'Durum'] = st.sidebar.selectbox(
        f"{row['İsim']}:", 
        ['Mevcut', 'Sevkli', 'İzinli'], 
        index=0, 
        key=f"status_{i}"
    )

# 3. BÖLÜM: GÖREV DAĞITIM AYARI
st.subheader("Bugünkü Nöbeti Hazırla")
ggm_vakit = st.radio("GGM Vakti:", ["Gündüz (1 Kişi)", "Akşam (2 Kişi)"], horizontal=True)
ggm_sayisi = 1 if "Gündüz" in ggm_vakit else 2

if st.button("Nöbet Çizelgesini Oluştur (Adil Dağıtım)"):
    mevcutlar = df[df['Durum'] == 'Mevcut'].copy()
    
    if len(mevcutlar) < 7: # Minimum gerekli adam sayısı (Niz:2, Kam:2, GGM:1, Gök:2)
        st.error("Hata: Mevcut personel sayısı görevleri doldurmaya yetmiyor!")
    else:
        def gorev_ata(liste, gorev_kolonu, adet):
            # O görevde en az sayıyı yapanı bul, eşitlikte toplam nöbetine bak
            secilenler = liste.sort_values(by=[gorev_kolonu]).head(adet)
            return secilenler.index.tolist()

        cizelge = {}
        
        # 1. Nizamiye (2 Kişi)
        niz_idx = gorev_ata(mevcutlar, 'Nizamiye', 2)
        cizelge['Nizamiye (2)'] = df.loc[niz_idx, 'İsim'].tolist()
        df.loc[niz_idx, 'Nizamiye'] += 1
        mevcutlar = mevcutlar.drop(niz_idx)

        # 2. Kamera (2 Kişi)
        kam_idx = gorev_ata(mevcutlar, 'Kamera', 2)
        cizelge['Kamera (2)'] = df.loc[kam_idx, 'İsim'].tolist()
        df.loc[kam_idx, 'Kamera'] += 1
        mevcutlar = mevcutlar.drop(kam_idx)

        # 3. GGM (1 veya 2 Kişi)
        ggm_idx = gorev_ata(mevcutlar, 'GGM', ggm_sayisi)
        cizelge['GGM'] = df.loc[ggm_idx, 'İsim'].tolist()
        df.loc[ggm_idx, 'GGM'] += 1
        mevcutlar = mevcutlar.drop(ggm_idx)

        # 4. GÖKSEM (2 Kişi)
        gok_idx = gorev_ata(mevcutlar, 'GÖKSEM', 2)
        cizelge['GÖKSEM (2)'] = df.loc[gok_idx, 'İsim'].tolist()
        df.loc[gok_idx, 'GÖKSEM'] += 1
        mevcutlar = mevcutlar.drop(gok_idx)

        # 5. Yaya Devriye (Geriye Kalanlar)
        cizelge['Yaya Devriye'] = mevcutlar['İsim'].tolist()
        df.loc[mevcutlar.index, 'Yaya_Devriye'] += 1

        # Sonucu Göster
        st.success("Nöbet Listesi Hazırlandı")
        # Listeleri görsel olarak güzelleştirmek için tabloya çevir
        max_len = max(len(v) for v in cizelge.values())
        for k in cizelge:
            while len(cizelge[k]) < max_len:
                cizelge[k].append("-")
        
        st.table(pd.DataFrame(cizelge))

# 4. BÖLÜM: SAYACLARI GÖSTER
st.subheader("Personel Görev İstatistikleri (Toplam Sayılar)")
st.dataframe(df.sort_values(by="İsim"))

if st.button("Tüm Sayaçları Sıfırla"):
    for col in ['Nizamiye', 'Kamera', 'GGM', 'GÖKSEM', 'Yaya_Devriye']:
        df[col] = 0
    st.rerun()
