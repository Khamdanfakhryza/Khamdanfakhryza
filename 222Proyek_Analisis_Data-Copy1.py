import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache_data
def load_air_quality_data():
    dataset_paths = {
        "All": "../clean_df_all.csv",
        "Aotizhongxin": "../Air-quality-dataset/PRSA_Data_Aotizhongxin_20130301-20170228.csv",
        "Changping": "../Air-quality-dataset/PRSA_Data_Changping_20130301-20170228.csv",
        "Dingling": "../Air-quality-dataset/PRSA_Data_Dingling_20130301-20170228.csv",
        "Dongsi": "../Air-quality-dataset/PRSA_Data_Dongsi_20130301-20170228.csv",
    }
    
    data_frames = {key: pd.read_csv(path) for key, path in dataset_paths.items()}
    data_frames["All"]["date_time"] = pd.to_datetime(data_frames["All"]["date_time"])
    return data_frames

data = load_air_quality_data()

st.sidebar.image("../images/logo.png")
st.sidebar.title("Navigasi")
page = st.sidebar.radio("Pilih Halaman:", ["Beranda", "Dataset", "Analisis 1", "Analisis 2", "Kesimpulan"])

if page == "Beranda":
    st.title("Analisis Kualitas Udara")
    st.markdown("""
    **Proyek Data:** Kualitas Udara
    
    **Nama:** Khamdan Annas Fakhryza  
    **Email:** Khamdan@std.unissul.ac.id
    """)
    st.subheader("Ringkasan Data")
    st.write(data["All"].describe())
    st.subheader("Pratinjau Data")
    st.dataframe(data["All"].head())

elif page == "Dataset":
    dataset_choice = st.sidebar.selectbox("Pilih Dataset:", list(data.keys())[1:])
    st.title(f"Dataset {dataset_choice}")
    st.write(data[dataset_choice].describe())
    st.dataframe(data[dataset_choice].head())

elif page == "Analisis 1":
    st.title("Hubungan Kecepatan Angin dengan PM2.5")
    df = data["All"]
    df["bulan"] = df["date_time"].dt.month
    musim_panas = df[df["bulan"].isin([6, 7, 8])]
    
    plt.figure(figsize=(10, 5))
    sns.scatterplot(x="WSPM", y="PM2.5", data=musim_panas)
    plt.title("Pengaruh Kecepatan Angin terhadap PM2.5 (Musim Panas)")
    st.pyplot(plt)

elif page == "Analisis 2":
    st.title("Dampak NO2 dan CO terhadap Kualitas Udara")
    df = data["All"]
    df["bulan"] = df["date_time"].dt.to_period("M")
    rata_bulanan = df.groupby("bulan").agg({"CO": "mean", "NO2": "mean", "PM2.5": "mean"}).reset_index()
    
    plt.figure(figsize=(10, 5))
    sns.lineplot(x="bulan", y="CO", data=rata_bulanan, label="CO", color="blue")
    sns.lineplot(x="bulan", y="NO2", data=rata_bulanan, label="NO2", color="red")
    sns.lineplot(x="bulan", y="PM2.5", data=rata_bulanan, label="PM2.5", color="green")
    plt.xticks(rotation=45)
    plt.title("Rata-rata Konsentrasi Polutan Per Bulan")
    st.pyplot(plt)

elif page == "Kesimpulan":
    st.title("Kesimpulan Analisis")
    st.markdown("""
    **Kesimpulan:**
    1. Kecepatan angin berperan dalam penyebaran polutan, terutama PM2.5.
    2. Peningkatan NO2 dan CO menandakan tingginya aktivitas kendaraan bermotor.
    3. Polutan tertentu menunjukkan pola musiman yang dapat dianalisis lebih lanjut.
    """)
