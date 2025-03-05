import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

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
st.markdown("---")

# ==========================================
# Memuat Data yang Sudah Dibersihkan
# ==========================================
@st.cache_data
def load_clean_data():
    df = pd.read_csv("clean_air_quality.csv")  # Gunakan dataset yang sudah siap
    df['date_time'] = pd.to_datetime(df['date_time'])
    return df

df_all = load_clean_data()

# ==========================================
# Sidebar & Navigasi
# ==========================================
st.sidebar.header("Navigasi Analisis")
analysis_option = st.sidebar.radio(
    "Pilih Analisis:",
    ["Dashboard Utama", "Kesimpulan"]
)

st.sidebar.markdown("---")
selected_location = st.sidebar.selectbox("Pilih Lokasi:", df_all['location'].unique())
date_range = st.sidebar.slider("Pilih Rentang Waktu:",
                               min_value=df_all['date_time'].min().date(),
                               max_value=df_all['date_time'].max().date(),
                               value=(df_all['date_time'].min().date(), df_all['date_time'].max().date()))

# Filter data berdasarkan lokasi dan rentang waktu
filtered_data = df_all[(df_all['location'] == selected_location) &
                       (df_all['date_time'].dt.date.between(date_range[0], date_range[1]))]

# ==========================================
# Dashboard Utama
# ==========================================
if analysis_option == "Dashboard Utama":
    st.header("📈 Dashboard Utama")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Data Points", f"{len(filtered_data):,}")
    with col2:
        st.metric("Lokasi Terpilih", selected_location)
    with col3:
        st.metric("Rentang Waktu", f"{date_range[0]} - {date_range[1]}")
    
    st.markdown("---")
    
    # Visualisasi 1: Tren PM2.5
    st.subheader("📊 Tren PM2.5 dalam Rentang Waktu")
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=filtered_data, x='date_time', y='PM2.5', ax=ax1)
    plt.xticks(rotation=45)
    st.pyplot(fig1)
    
    # Visualisasi 2: Korelasi Polutan
    st.subheader("🔗 Korelasi Antar Polutan")
    corr_matrix = filtered_data[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].corr()
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, ax=ax2)
    st.pyplot(fig2)

# ==========================================
# Kesimpulan
# ==========================================
if analysis_option == "Kesimpulan":
    st.header("📌 Kesimpulan Utama")
    st.markdown("""
    ### 1. Tren PM2.5
    - Konsentrasi PM2.5 cenderung lebih tinggi pada bulan-bulan musim dingin.
    - Penurunan PM2.5 terlihat di musim panas, kemungkinan karena hujan lebih sering.
    
    ### 2. Korelasi Polutan
    - PM2.5 memiliki korelasi tinggi dengan PM10 dan NO2, menunjukkan pengaruh aktivitas kendaraan.
    - Ozon (O3) menunjukkan korelasi negatif dengan NO2, mencerminkan reaksi fotokimia.
    
    ### 3. Pengaruh Kecepatan Angin
    - Kecepatan angin lebih tinggi cenderung menurunkan konsentrasi PM2.5.
    
    ### 4. Pengaruh Curah Hujan
    - Curah hujan yang tinggi secara signifikan menurunkan konsentrasi PM2.5.
    """)
