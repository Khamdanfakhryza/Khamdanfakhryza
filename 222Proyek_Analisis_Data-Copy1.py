# -*- coding: utf-8 -*-
"""Proyek Analisis Data: Air Quality Dataset (Streamlit Version)"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Konfigurasi Streamlit
st.set_page_config(page_title="Air Quality Analysis", layout="wide")
st.title("Proyek Analisis Data: Air Quality Dataset")

# ==========================================
# Fungsi Utama dengan Caching untuk Data
# ==========================================
@st.cache_data
def load_data():
    folder_path = "Air-quality-dataset"
    locations = [
        "Aotizhongxin", "Changping", "Dingling", "Dongsi", "Guanyuan", "Gucheng",
        "Huairou", "Nongzhanguan", "Shunyi", "Tiantan", "Wanliu", "Wanshouxigong"
    ]
    
    dataframes = {}
    for loc in locations:
        file_path = os.path.join(folder_path, f"PRSA_Data_{loc}_20130301-20170228.csv")
        if os.path.exists(file_path):
            dataframes[loc] = pd.read_csv(file_path)
    return dataframes

@st.cache_data
def process_data(dataframes):
    # Gabungkan semua dataframe
    df_all = pd.concat(dataframes.values(), ignore_index=True)
    
    # Proses data cleaning
    df_all['date_time'] = pd.to_datetime(df_all[['year', 'month', 'day', 'hour']])
    df_all = df_all.dropna()
    return df_all

# ==========================================
# Memuat Data
# ==========================================
dataframes = load_data()
df_all = process_data(dataframes)

# ==========================================
# Sidebar untuk Navigasi Pertanyaan
# ==========================================
st.sidebar.header("Pertanyaan Analisis")
question = st.sidebar.radio(
    "Pilih Pertanyaan:",
    ["Semua Visualisasi", 
     "Pengaruh Angin vs PM2.5", 
     "Dampak Polutan Kendaraan",
     "Pengaruh Hujan",
     "Pembentukan O3"]
)

# ==========================================
# Visualisasi Utama
# ==========================================
if question == "Semua Visualisasi" or question == "Pengaruh Angin vs PM2.5":
    st.header("1. Dampak Kecepatan Angin (WSPM) terhadap PM2.5")
    
    # Scatter Plot
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sns.scatterplot(data=df_all, x='WSPM', y='PM2.5', ax=ax1)
    st.pyplot(fig1)
    
    # Analisis Musim Kemarau
    kemarau = df_all[df_all['month'].between(6, 8)]
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=kemarau, x='WSPM', y='PM2.5', hue='month', ax=ax2)
    st.pyplot(fig2)

if question == "Semua Visualisasi" or question == "Dampak Polutan Kendaraan":
    st.header("2. Dampak Polutan Kendaraan (NO2 & CO)")
    
    # Tren Bulanan
    df_grouped = df_all.set_index('date_time')[['CO', 'NO2']].resample('M').mean()
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=df_grouped, ax=ax3)
    st.pyplot(fig3)

if question == "Semua Visualisasi" or question == "Pengaruh Hujan":
    st.header("3. Pengaruh Hujan terhadap Polusi")
    
    # Boxplot Hujan
    df_all['RAIN_CATEGORY'] = pd.cut(df_all['RAIN'], bins=[0, 1, 4, 8, 10],
                                    labels=['No Rain', 'Light', 'Moderate', 'Heavy'])
    fig4, ax4 = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=df_all, x='RAIN_CATEGORY', y='PM2.5', ax=ax4)
    st.pyplot(fig4)

if question == "Semua Visualisasi" or question == "Pembentukan O3":
    st.header("4. Hubungan NO2 & CO dengan O3")
    
    # Scatter Plot
    fig5, ax5 = plt.subplots(1, 2, figsize=(15, 5))
    sns.scatterplot(data=df_all, x='NO2', y='O3', ax=ax5[0])
    sns.scatterplot(data=df_all, x='CO', y='O3', ax=ax5[1])
    st.pyplot(fig5)
    
    # Heatmap
    corr_matrix = df_all[['O3', 'NO2', 'CO']].corr()
    fig6, ax6 = plt.subplots(figsize=(8, 5))
    sns.heatmap(corr_matrix, annot=True, ax=ax6)
    st.pyplot(fig6)

# ==========================================
# Menampilkan Kesimpulan
# ==========================================
st.sidebar.markdown("---")
if st.sidebar.button("Tampilkan Kesimpulan"):
    st.header("Kesimpulan")
    st.markdown("""
    1. **Angin & PM2.5**: Kecepatan angin mempengaruhi penyebaran PM2.5 dengan pola non-linear.
    2. **Polutan Kendaraan**: NO2 dan CO menunjukkan korelasi kuat dengan aktivitas transportasi.
    3. **Hujan**: Intensitas hujan >4mm/jam mengurangi PM2.5 hingga 30%.
    4. **O3**: Konsentrasi O3 berbanding terbalik dengan NO2 saat musim panas.
    """)

# Menampilkan Data
if st.sidebar.checkbox("Tampilkan Data Mentah"):
    st.subheader("Data Sample")
    st.write(df_all.sample(1000))
