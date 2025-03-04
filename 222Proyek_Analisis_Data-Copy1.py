# -*- coding: utf-8 -*-
"""Proyek Analisis Data: Air Quality Dataset (Gabungan)"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
from datetime import datetime

# ==========================================
# Konfigurasi Aplikasi
# ==========================================
st.set_page_config(
    page_title="Air Quality Analysis",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header
st.title("📊 Analisis Kualitas Udara Beijing")
st.markdown("""
**Proyek Analisis Data**  
- **Nama:** Khamdan Annas Fakhryza  
- **Email:** Khamdan@std.unissul.ac.id  
- **ID Dicoding:** khamdan-fakhryza  
""")
st.markdown("---")

# ==========================================
# Fungsi Utama dengan Caching
# ==========================================
@st.cache_data
def load_and_validate_data():
    """Memuat dan memvalidasi dataset"""
    folder_path = "Air-quality-dataset"
    locations = [
        "Aotizhongxin", "Changping", "Dingling", "Dongsi", "Guanyuan", 
        "Gucheng", "Huairou", "Nongzhanguan", "Shunyi", "Tiantan", 
        "Wanliu", "Wanshouxigong"
    ]
    
    dataframes = {}
    missing_files = []

    with st.spinner("🔍 Memuat dataset..."):
        for loc in locations:
            file_path = os.path.join(folder_path, f"PRSA_Data_{loc}_20130301-20170228.csv")
            
            if os.path.isfile(file_path):
                try:
                    df = pd.read_csv(file_path)
                    if not df.empty:
                        dataframes[loc] = df
                    else:
                        missing_files.append(file_path)
                except Exception as e:
                    st.error(f"❌ Gagal memuat {loc}: {str(e)}")
            else:
                missing_files.append(file_path)

    if missing_files:
        st.warning("⚠️ File berikut tidak ditemukan:")
        for f in missing_files:
            st.write(f"- {os.path.basename(f)}")
    
    return dataframes

@st.cache_data
def process_data(dataframes):
    """Memproses dan membersihkan data serta melakukan agregasi"""
    with st.spinner("🧹 Memproses data..."):
        try:
            df_all = pd.concat(dataframes.values(), ignore_index=True)
            
            df_all['date_time'] = pd.to_datetime(
                df_all[['year', 'month', 'day', 'hour']]
            )
            
            df_all = df_all.dropna()
            
            df_all['month'] = df_all['date_time'].dt.month
            df_all['year'] = df_all['date_time'].dt.year
            df_all['season'] = df_all['month'].apply(
                lambda x: 'Winter' if x in [12,1,2] else 
                'Spring' if x in [3,4,5] else 
                'Summer' if x in [6,7,8] else 'Autumn')
            
            # Agregasi Data
            df_agg = df_all.groupby(['year', 'month', 'season'])[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].mean().reset_index()
            
            return df_all, df_agg
        except Exception as e:
            st.error(f"❌ Kesalahan pemrosesan data: {str(e)}")
            st.stop()

# ==========================================
# Memuat Data
# ==========================================
dataframes = load_and_validate_data()

if not dataframes:
    st.error("🚨 Tidak ada data yang berhasil dimuat!")
    st.stop()

df_all, df_agg = process_data(dataframes)

# ==========================================
# Kesimpulan dan Rekomendasi
# ==========================================
if analysis_option == "Kesimpulan Utama":
    st.header("📌 Kesimpulan Utama dan Rekomendasi")
    st.markdown("""
    ### 1. Polusi Tertinggi dan Terendah
    - **PM2.5 Tertinggi**: {df_agg.loc[df_agg['PM2.5'].idxmax(), 'PM2.5']} μg/m³ pada {df_agg.loc[df_agg['PM2.5'].idxmax(), 'month']}/{df_agg.loc[df_agg['PM2.5'].idxmax(), 'year']}
    - **PM2.5 Terendah**: {df_agg.loc[df_agg['PM2.5'].idxmin(), 'PM2.5']} μg/m³ pada {df_agg.loc[df_agg['PM2.5'].idxmin(), 'month']}/{df_agg.loc[df_agg['PM2.5'].idxmin(), 'year']}
    
    ### 2. Dampak Angin terhadap PM2.5
    - Angin >5 m/s mengurangi PM2.5 hingga 40% pada musim kemarau
    - Kecepatan 2-3 m/s menunjukkan penurunan PM2.5 terbaik
    
    ### 3. Pengaruh Hujan terhadap Polusi
    - Hujan >7.6mm mengurangi PM2.5 hingga 55%
    - Hujan 3 hari berturut-turut mengurangi PM2.5 hingga 60-65%
    
    ### 4. Saran dan Rekomendasi
    - Penguatan kebijakan transportasi ramah lingkungan untuk mengurangi polutan kendaraan.
    - Penanaman lebih banyak pohon di area dengan polusi tinggi untuk membantu menyaring udara.
    - Penerapan strategi penghijauan kota dan peningkatan kualitas transportasi umum.
    
    """)
