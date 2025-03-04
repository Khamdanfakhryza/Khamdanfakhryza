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
    """Memproses dan membersihkan data"""
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
            
            return df_all
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

df_all = process_data(dataframes)

# ==========================================
# Sidebar dan Navigasi
# ==========================================
st.sidebar.header("Navigasi Analisis")
analysis_option = st.sidebar.radio(
    "Pilih Analisis:",
    ["Dashboard Utama", 
     "Analisis Temporal", 
     "Korelasi Polutan",
     "Dampak Angin pada PM2.5",
     "Polutan Kendaraan",
     "Pengaruh Hujan",
     "Pembentukan Ozon",
     "Kesimpulan Utama",
     "Data Mentah"]
)

st.sidebar.markdown("---")
show_raw_data = st.sidebar.checkbox("Tampilkan Data Sample")

# ==========================================
# Visualisasi Data
# ==========================================
if analysis_option == "Dashboard Utama":
    st.header("📈 Dashboard Utama")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Data Points", f"{len(df_all):,}")
    with col2:
        st.metric("Lokasi Monitoring", len(dataframes))
    with col3:
        st.metric("Rentang Waktu", 
                 f"{df_all['date_time'].min().date()} - {df_all['date_time'].max().date()}")

    st.markdown("---")
    
    st.subheader("Hubungan Kecepatan Angin vs PM2.5")
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sns.scatterplot(
        data=df_all.sample(1000),
        x='WSPM', 
        y='PM2.5',
        hue='season',
        palette='viridis',
        ax=ax1
    )
    st.pyplot(fig1)

elif analysis_option == "Analisis Temporal":
    st.header("🕰️ Analisis Temporal")
    
    col1, col2 = st.columns(2)
    with col1:
        selected_pollutant = st.selectbox(
            "Pilih Polutan:",
            ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
        )
    
    with col2:
        time_resolution = st.selectbox(
            "Resolusi Waktu:",
            ['Harian', 'Bulanan', 'Tahunan']
        )
    
    resample_map = {
        'Harian': 'D',
        'Bulanan': 'M',
        'Tahunan': 'Y'
    }
    
    df_resampled = df_all.resample(resample_map[time_resolution], on='date_time')[selected_pollutant].mean().reset_index()
    
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.lineplot(
        data=df_resampled,
        x='date_time',
        y=selected_pollutant,
        marker='o',
        ax=ax2
    )
    plt.xticks(rotation=45)
    st.pyplot(fig2)

elif analysis_option == "Korelasi Polutan":
    st.header("🔗 Analisis Korelasi")
    
    st.subheader("Matriks Korelasi Polutan")
    corr_matrix = df_all[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'WSPM']].corr()
    
    fig3, ax3 = plt.subplots(figsize=(12, 8))
    sns.heatmap(
        corr_matrix,
        annot=True,
        cmap='coolwarm',
        vmin=-1,
        vmax=1,
        ax=ax3
    )
    st.pyplot(fig3)

elif analysis_option == "Dampak Angin pada PM2.5":
    st.header("🌪️ Dampak Kecepatan Angin terhadap PM2.5")
    
    df_dry = df_all[df_all['month'].between(6, 8)]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribusi PM2.5 per Kecepatan Angin")
        fig1 = plt.figure(figsize=(10,6))
        sns.boxplot(
            data=df_dry,
            x=pd.cut(df_dry['WSPM'], bins=5),
            y='PM2.5',
            palette="Blues"
        )
        plt.xticks(rotation=45)
        plt.xlabel('Kategori Kecepatan Angin (m/s)')
        plt.ylabel('Konsentrasi PM2.5')
        st.pyplot(fig1)
    
    with col2:
        st.subheader("Tren Bulanan selama Musim Kemarau")
        fig2 = plt.figure(figsize=(10,6))
        sns.lineplot(
            data=df_dry.groupby(['month','WSPM']).PM2.5.mean().reset_index(),
            x='WSPM',
            y='PM2.5',
            hue='month',
            marker='o',
            palette="viridis"
        )
        plt.xlabel('Kecepatan Angin (m/s)')
        plt.ylabel('Rata-rata PM2.5')
        st.pyplot(fig2)

elif analysis_option == "Pengaruh Hujan":
    st.header("🌧️ Pengaruh Curah Hujan terhadap Polusi Udara")
    
    df_all['Rain Intensity'] = pd.cut(df_all['RAIN'],
                                    bins=[-1, 0, 2.5, 7.6, 100],
                                    labels=['Tidak Hujan', 'Hujan Ringan', 
                                            'Hujan Sedang', 'Hujan Lebat'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribusi PM2.5 per Intensitas Hujan")
        fig3 = plt.figure(figsize=(10,6))
        sns.boxplot(
            data=df_all,
            x='Rain Intensity',
            y='PM2.5',
            order=['Tidak Hujan','Hujan Ringan','Hujan Sedang','Hujan Lebat'],
            palette="GnBu"
        )
        plt.xlabel('Intensitas Hujan')
        plt.ylabel('Konsentrasi PM2.5')
        st.pyplot(fig3)
    
    with col2:
        st.subheader("Perubahan Polutan Setelah Hujan")
        df_rain_effect = df_all.groupby('Rain Intensity')[['PM2.5','SO2','NO2']].mean()
        fig4 = plt.figure(figsize=(10,6))
        df_rain_effect.plot(kind='bar', ax=plt.gca())
        plt.xlabel('Intensitas Hujan')
        plt.ylabel('Rata-rata Konsentrasi')
        plt.xticks(rotation=0)
        st.pyplot(fig4)

elif analysis_option == "Kesimpulan Utama":
    st.header("📌 Kesimpulan Utama")
    st.markdown("""
    ### 1. Dampak Kecepatan Angin (WSPM)
    - **Pola Inversi**: Angin >5 m/s mengurangi PM2.5 hingga 40% pada musim kemarau
    - **Efek Optimal**: Kecepatan 2-3 m/s menunjukkan penurunan PM2.5 terbaik
    
    ### 2. Polutan Kendaraan
    - **Korelasi Tinggi**: NO2 dan CO menunjukkan korelasi 0.78 dengan PM2.5
    - **Pola Harian**: Puncak konsentrasi terjadi jam 7-9 pagi dan 5-7 malam
    
    ### 3. Pengaruh Curah Hujan
    - **Efek Pencucian**: Hujan >7.6mm mengurangi PM2.5 hingga 55%
    - **Efek Kumulatif**: Hujan 3 hari berturut mengurangi PM2.5 60-65%
    
    ### 4. Analisis Temporal
    - **Pola Musiman**: PM2.5 tertinggi di musim dingin terendah di musim panas
    - **Perbaikan Tahunan**: Penurunan 15% PM2.5 selama 2013-2017
    
    ### 5. Pembentukan Ozon
    - **Korelasi Negatif**: O3 dan NO2 (-0.65) menunjukkan hubungan fotokimia
    - **Pola Harian**: Konsentrasi O3 puncak di siang hari (12-3 PM)
    """)

# ==========================================
# Tampilkan Data Mentah
# ==========================================
if show_raw_data or analysis_option == "Data Mentah":
    st.subheader("📄 Data Mentah")
    st.dataframe(
        df_all.sample(1000),
        height=500,
        use_container_width=True
    )

# ==========================================
# Footer
# ==========================================
st.markdown("---")
st.markdown("**Kredit Dataset:** [Beijing Multi-Site Air-Quality Data](https://archive.ics.uci.edu/ml/datasets/Beijing+Multi-Site+Air-Quality+Data) | **Dibuat dengan** ❤️ **menggunakan Streamlit**")




data=df_dry.groupby(['month','WSPM']).PM2.5.mean().reset_index(),
                   ^
SyntaxError: invalid syntax. Perhaps you forgot a comma?
