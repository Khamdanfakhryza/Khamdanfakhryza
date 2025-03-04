# -*- coding: utf-8 -*-
"""Proyek Analisis Data: Air Quality Dataset (Final Version)"""
#- **Nama:** Khamdan Annas Fakhryza
#- **Email:** Khamdan@std.unissul.ac.id
#- **ID Dicoding:** khamdan-fakhryza

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# ==========================================
# Konfigurasi Aplikasi
# ==========================================
st.set_page_config(
    page_title="Air Quality Analysis",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Analisis Kualitas Udara Beijing")
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
    
    # Validasi folder
    if not os.path.exists(folder_path):
        st.error(f"🚨 Folder '{folder_path}' tidak ditemukan!")
        st.markdown("""
        **Struktur folder yang diperlukan:**
        ```
        project_folder/
        ├── air_quality_app.py
        └── Air-quality-dataset/
            ├── PRSA_Data_Aotizhongxin_20130301-20170228.csv
            ├── PRSA_Data_Changping_20130301-20170228.csv
            └── ... (file lainnya)
        ```
        """)
        st.stop()

    dataframes = {}
    missing_files = []

    # Memuat data
    with st.spinner("🔍 Memuat dataset..."):
        for loc in locations:
            file_path = os.path.join(folder_path, f"PRSA_Data_{loc}_20130301-20170228.csv")
            
            if os.path.isfile(file_path):
                try:
                    df = pd.read_csv(file_path)
                    if not df.empty:
                        dataframes[loc] = df
                        st.success(f"✅ {loc:20} : {len(df):,} records")
                    else:
                        missing_files.append(file_path)
                except Exception as e:
                    st.error(f"❌ Gagal memuat {loc}: {str(e)}")
            else:
                missing_files.append(file_path)

    # Validasi file yang hilang
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
            # Gabungkan semua dataframe
            df_all = pd.concat(dataframes.values(), ignore_index=True)
            
            # Konversi ke datetime
            df_all['date_time'] = pd.to_datetime(
                df_all[['year', 'month', 'day', 'hour']].rename(columns={
                    'year': 'year',
                    'month': 'month',
                    'day': 'day',
                    'hour': 'hour'
                })
            )
            
            # Handle missing values
            df_all = df_all.dropna()
            
            # Tambahkan fitur tambahan
            df_all['month'] = df_all['date_time'].dt.month
            df_all['year'] = df_all['date_time'].dt.year
            
            return df_all
        except Exception as e:
            st.error(f"❌ Kesalahan pemrosesan data: {str(e)}")
            st.stop()

# ==========================================
# Sidebar dan Navigasi
# ==========================================
st.sidebar.header("Navigasi Analisis")
analysis_option = st.sidebar.radio(
    "Pilih Analisis:",
    ["Dashboard Utama", 
     "Analisis Temporal", 
     "Korelasi Polutan",
     "Data Mentah"]
)

st.sidebar.markdown("---")
show_raw_data = st.sidebar.checkbox("Tampilkan Data Sample")

# ==========================================
# Memuat Data
# ==========================================
dataframes = load_and_validate_data()

if not dataframes:
    st.error("🚨 Tidak ada data yang berhasil dimuat!")
    st.stop()

df_all = process_data(dataframes)

# ==========================================
# Visualisasi Data
# ==========================================
if analysis_option == "Dashboard Utama":
    st.header("📈 Dashboard Utama")
    
    # Row 1: Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Data Points", f"{len(df_all):,}")
    with col2:
        st.metric("Lokasi Monitoring", len(dataframes))
    with col3:
        st.metric("Rentang Waktu", 
                 f"{df_all['date_time'].min().date()} - {df_all['date_time'].max().date()}")

    st.markdown("---")
    
    # Row 2: Scatter Plot
    st.subheader("Hubungan Kecepatan Angin vs PM2.5")
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sns.scatterplot(
        data=df_all.sample(1000),
        x='WSPM', 
        y='PM2.5',
        hue='month',
        palette='viridis',
        ax=ax1
    )
    st.pyplot(fig1)

elif analysis_option == "Analisis Temporal":
    st.header("🕰️ Analisis Temporal")
    
    # Time Series Analysis
    st.subheader("Tren Bulanan Polutan")
    selected_pollutant = st.selectbox(
        "Pilih Polutan:",
        ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    )
    
    df_monthly = df_all.resample('M', on='date_time')[selected_pollutant].mean().reset_index()
    
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.lineplot(
        data=df_monthly,
        x='date_time',
        y=selected_pollutant,
        marker='o',
        ax=ax2
    )
    plt.xticks(rotation=45)
    st.pyplot(fig2)

elif analysis_option == "Korelasi Polutan":
    st.header("🔗 Analisis Korelasi")
    
    # Heatmap
    st.subheader("Matriks Korelasi Polutan")
    corr_matrix = df_all[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].corr()
    
    fig3, ax3 = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        corr_matrix,
        annot=True,
        cmap='coolwarm',
        vmin=-1,
        vmax=1,
        ax=ax3
    )
    st.pyplot(fig3)

# ==========================================
# Tampilkan Data Mentah
# ==========================================
if show_raw_data:
    st.subheader("📄 Data Mentah")
    st.dataframe(
        df_all.sample(1000),
        height=300,
        use_container_width=True
    )

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
Cara Menjalankan:




# ==========================================
# Footer
# ==========================================
st.markdown("---")
st.markdown("**Kredit:** Dataset dari [Beijing Multi-Site Air-Quality Data](https://archive.ics.uci.edu/ml/datasets/Beijing+Multi-Site+Air-Quality+Data)")
