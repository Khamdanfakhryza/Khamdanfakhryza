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
def load_clean_data():
    df = pd.read_csv("clean_air_quality.csv")  # Gunakan dataset yang sudah siap
    df['date_time'] = pd.to_datetime(df['date_time'])
    return df

df_all = load_clean_data()

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
st.sidebar.header("Navigasi Analisis")
selected_location = st.sidebar.selectbox("Pilih Lokasi:", df_all['location'].unique())
date_range = st.sidebar.slider("Pilih Rentang Waktu:",
                               min_value=df_all['date_time'].min().date(),
                               max_value=df_all['date_time'].max().date(),
                               value=(df_all['date_time'].min().date(), df_all['date_time'].max().date()))

# Filter data berdasarkan lokasi dan rentang waktu
filtered_data = df_all[(df_all['location'] == selected_location) &
                       (df_all['date_time'].dt.date.between(date_range[0], date_range[1]))]

if analysis_option == "Dashboard Utama":  # ✅ Perbaikan: Tambahkan `if` sebelum indentasi
    st.header("📈 Dashboard Utama")

    col1, col2, col3 = st.columns(3)  # ✅ Indentasi benar
    with col1:
        st.metric("Total Data Points", f"{len(filtered_data):,}")  # ✅ Gunakan `filtered_data`
    with col2:
        st.metric("Lokasi Terpilih", selected_location)
    with col3:
        st.metric("Rentang Waktu", 
                 f"{date_range[0]} - {date_range[1]}")

    st.markdown("---")
    
    st.subheader("📊 Tren PM2.5 dalam Rentang Waktu")
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=filtered_data, x='date_time', y='PM2.5', ax=ax1)
    plt.xticks(rotation=45)
    st.pyplot(fig1)

    st.subheader("🔗 Korelasi Antar Polutan")
    corr_matrix = filtered_data[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].corr()
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, ax=ax2)
    st.pyplot(fig2)

elif analysis_option == "Analisis Temporal":  # ✅ Pastikan sejajar dengan `if`
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
    
    df_resampled = filtered_data.resample(resample_map[time_resolution], on='date_time')[selected_pollutant].mean().reset_index()
    
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

elif analysis_option == "Korelasi Polutan":  # ✅ Pastikan sejajar dengan `if`
    st.header("🔗 Analisis Korelasi")
    
    st.subheader("Matriks Korelasi Polutan")
    corr_matrix = filtered_data[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'WSPM']].corr()
    
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
            data = df_dry.groupby(['month', 'WSPM'])['PM2.5'].mean().reset_index(),
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
    ### 1. Tren PM2.5
    - Konsentrasi PM2.5 cenderung lebih tinggi pada musim dingin.
    - Penurunan PM2.5 terlihat di musim panas, kemungkinan karena hujan lebih sering.

    ### 2. Korelasi Polutan
    - PM2.5 memiliki korelasi tinggi dengan PM10 dan NO2, menunjukkan pengaruh aktivitas kendaraan.
    - Ozon (O3) menunjukkan korelasi negatif dengan NO2, mencerminkan reaksi fotokimia.

    ### 3. Pengaruh Kecepatan Angin
    - Kecepatan angin lebih tinggi cenderung menurunkan konsentrasi PM2.5.

    ### 4. Pengaruh Curah Hujan
    - Curah hujan yang tinggi secara signifikan menurunkan konsentrasi PM2.5.
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
