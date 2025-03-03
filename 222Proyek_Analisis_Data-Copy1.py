# %%
"""
# Proyek Analisis Data: Air Quality Dataset
- **Nama:** Khamdan Annas Fakhryza
- **Email:** Khamdan@std.unissul.ac.id
- **ID Dicoding:** khamdan-fakhryza
"""

# %%
"""
## Menentukan Pertanyaan Bisnis Atau Analisis
"""

# %%
"""
- 1. Apa dampak kecepatan angin (WSPM) terhadap distribusi konsentrasi PM2.5 selama muim panas (Juni hingga Agustus)?
- 2. Apa pengaruh kkonsentrasi NO2 dan CO yag berasal dari misi kedaraan bermotor terhadap kualitas udara?
- 3. Bagaimana hujan mempengaruhi tingkat polusi Udara akibat polutan tertentu?
- 4. Bagaimana kaitan antara konsentrasi NO2  dan CO  dalam P=rposes pembentukan O3 ?
"""

# %%
"""
## Import Semua Packages/Library yang Digunakan
"""

# %%
import numpy as np  # Untuk operasi numerik
import pandas as pd  # Untuk manipulasi data\import matplotlib.pyplot as plt  # Untuk visualisasi\import seaborn as sns  # Untuk plotting berbasis statistik
import warnings  # Untuk mengabaikan peringatan
import seaborn as sns
import matplotlib.pyplot as plt

# %%
"""
### Gathering Data
"""

# %%
import os
print(os.getcwd())  # Menampilkan direktori kerja saat ini


# %%
folder_path = "Air-quality-dataset"

# Menampilkan isi folder untuk memastikan file ada
import os
files_in_folder = os.listdir(folder_path)
print(files_in_folder)


# %%
import pandas as pd
import os

# Tentukan folder tempat file berada
folder_path = "Air-quality-dataset"  # Path ke folder lokal Anda

# Daftar lokasi
locations = [
    "Aotizhongxin", "Changping", "Dingling", "Dongsi", "Guanyuan", "Gucheng",
    "Huairou", "Nongzhanguan", "Shunyi", "Tiantan", "Wanliu", "Wanshouxigong"
]

# Membaca dataset ke dalam dictionary
dataframes = {}

for loc in locations:
    # Membuat path ke file
    file_path = os.path.join(folder_path, f"PRSA_Data_{loc}_20130301-20170228.csv")
    
    # Cek apakah file ada
    if os.path.exists(file_path):
        # Membaca file CSV
        dataframes[loc] = pd.read_csv(file_path)
        print(f"Loaded {loc} successfully!")
    else:
        print(f"File for {loc} not found at {file_path}")

# Sekarang, setiap lokasi memiliki dataframe tersimpan dalam dictionary `dataframes`
# Misalnya, data untuk Aotizhongxin bisa diakses dengan dataframes["Aotizhongxin"]


# %%
import pandas as pd

# Load the CSV files into DataFrames
df_Aotizhongxin = pd.read_csv('Air-quality-dataset/PRSA_Data_Aotizhongxin_20130301-20170228.csv')
df_Changping = pd.read_csv('Air-quality-dataset/PRSA_Data_Changping_20130301-20170228.csv')
df_Dingling = pd.read_csv('Air-quality-dataset/PRSA_Data_Dingling_20130301-20170228.csv')
df_Dongsi = pd.read_csv('Air-quality-dataset/PRSA_Data_Dongsi_20130301-20170228.csv')
df_Guanyuan = pd.read_csv('Air-quality-dataset/PRSA_Data_Guanyuan_20130301-20170228.csv')
df_Gucheng = pd.read_csv('Air-quality-dataset/PRSA_Data_Gucheng_20130301-20170228.csv')
df_Huairou = pd.read_csv('Air-quality-dataset/PRSA_Data_Huairou_20130301-20170228.csv')
df_Nongzhanguan = pd.read_csv('Air-quality-dataset/PRSA_Data_Nongzhanguan_20130301-20170228.csv')
df_Shunyi = pd.read_csv('Air-quality-dataset/PRSA_Data_Shunyi_20130301-20170228.csv')
df_Tiantan = pd.read_csv('Air-quality-dataset/PRSA_Data_Tiantan_20130301-20170228.csv')
df_Wanliu = pd.read_csv('Air-quality-dataset/PRSA_Data_Wanliu_20130301-20170228.csv')
df_Wanshouxigong = pd.read_csv('Air-quality-dataset/PRSA_Data_Wanshouxigong_20130301-20170228.csv')


# %%
import pandas as pd
import os

# Pastikan lokasi folder sesuai dengan lokasi tempat file diunduh oleh gdown
folder_path = "Air-quality-dataset"

# Daftar lokasi yang akan diproses
locations = [
    "Aotizhongxin", "Changping", "Dingling", "Dongsi", "Guanyuan", "Gucheng",
    "Huairou", "Nongzhanguan", "Shunyi", "Tiantan", "Wanliu", "Wanshouxigong"
]

# Membaca dataset ke dalam dictionary
dataframes = {}
for loc in locations:
    file_path = os.path.join(folder_path, f"PRSA_Data_{loc}_20130301-20170228.csv")

    if os.path.exists(file_path):  # Cek apakah file ada
        dataframes[loc] = pd.read_csv(file_path)
        print(f"✅ Loaded {loc} successfully!")
    else:
        print(f"❌ File for {loc} not found! Check the folder path.")

# Sekarang, setiap lokasi memiliki dataframe tersimpan dalam dictionary `dataframes`


# %%
dataframes["Aotizhongxin"].head(6)

# %%
"""
## Data Wrangling
"""

# %%
dataframes["Changping"].head(6)

# %%
dataframes["Dingling"].head(6)

# %%
dataframes["Dongsi"].head(6)

# %%
dataframes["Guanyuan"].head(6)

# %%
dataframes["Gucheng"].head(6)

# %%
dataframes["Huairou"].head(6)

# %%
dataframes["Nongzhanguan"].head(6)

# %%
dataframes["Shunyi"].head(6)

# %%
dataframes["Tiantan"].head(6)

# %%
dataframes["Wanliu"].head(6)

# %%
dataframes["Wanshouxigong"].head(6)

# %%
"""
### Assessing Data
"""

# %%
"""
Missing value
"""

# %%
for name, df in dataframes.items():
    print(f"\nDataframe {name}:")
    print(df.isnull().sum())


# %%
"""
Setelah menganalisis data yang mengandung nilai kosong berdasarkan beberapa kolom tertentu, ditemukan jumlah yang cukup banyak, sehingga perlu kita tangani pada tahap berikutnya.
"""

# %%
"""
Duplicate Data
"""

# %%
"""
Tidak ada data yang duplicated
"""

# %%
"""
Outlier
"""

# %%
import numpy as np
import pandas as pd

# Fungsi untuk mendeteksi outliers dengan metode IQR
def detect_outliers_iqr(data):
    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return ((data < lower_bound) | (data > upper_bound)).any(axis=1)

# Dictionary yang sudah ada dengan nama lokasi sebagai key dan DataFrame sebagai value
datasets = dataframes

# Mendeteksi outliers untuk setiap DataFrame di dictionary `dataframes`
for name, df in datasets.items():
    numeric_df = df.select_dtypes(include=[np.number])  # Mengambil kolom numeric saja
    outliers = detect_outliers_iqr(numeric_df)
    print(f"Outliers in {name} (IQR):\n", df[outliers])


# %%
"""
Boxplot
"""

# %%
# Mengakses DataFrame Aotizhongxin dari dictionary `dataframes`
df_Aotizhongxin = dataframes["Aotizhongxin"]

# Menyaring kolom numerik
numeric_columns = df_Aotizhongxin.select_dtypes(include='number').columns

# Menyiapkan figure untuk boxplot
plt.figure(figsize=(15, 10))

# Membuat boxplot untuk setiap kolom numerik
for i, column in enumerate(numeric_columns, 1):
    plt.subplot(len(numeric_columns), 1, i)
    sns.boxplot(x=df_Aotizhongxin[column])
    plt.title(f'Boxplot {column}')
    plt.xlabel(column)

plt.tight_layout()  # Menyusun layout agar tidak saling tumpang tindih
plt.show()


# %%
"""
Ada bebrapaOutlier yang cukup banyak yang dapat mempengaruhi analisis.
"""

# %%
"""
### Cleaning Data
"""

# %%
"""
Imputasi Isi Nilai Hilang dengan Mean
"""

# %%
"""
Pisahkan kolom numerik dari kolom non-numerik
"""

# %%
# Mengakses DataFrame dari dictionary 'dataframes' dan memisahkan kolom numerik dan non-numerik

numeric_Aotizhongxin = dataframes["Aotizhongxin"].select_dtypes(include=['number'])
non_numeric_Aotizhongxin = dataframes["Aotizhongxin"].select_dtypes(exclude=['number'])

numeric_Changping = dataframes["Changping"].select_dtypes(include=['number'])
non_numeric_Changping = dataframes["Changping"].select_dtypes(exclude=['number'])

numeric_Dingling = dataframes["Dingling"].select_dtypes(include=['number'])
non_numeric_Dingling = dataframes["Dingling"].select_dtypes(exclude=['number'])

numeric_Dongsi = dataframes["Dongsi"].select_dtypes(include=['number'])
non_numeric_Dongsi = dataframes["Dongsi"].select_dtypes(exclude=['number'])

numeric_Guanyuan = dataframes["Guanyuan"].select_dtypes(include=['number'])
non_numeric_Guanyuan = dataframes["Guanyuan"].select_dtypes(exclude=['number'])

numeric_Gucheng = dataframes["Gucheng"].select_dtypes(include=['number'])
non_numeric_Gucheng = dataframes["Gucheng"].select_dtypes(exclude=['number'])

numeric_Huairou = dataframes["Huairou"].select_dtypes(include=['number'])
non_numeric_Huairou = dataframes["Huairou"].select_dtypes(exclude=['number'])

numeric_Nongzhanguan = dataframes["Nongzhanguan"].select_dtypes(include=['number'])
non_numeric_Nongzhanguan = dataframes["Nongzhanguan"].select_dtypes(exclude=['number'])

numeric_Shunyi = dataframes["Shunyi"].select_dtypes(include=['number'])
non_numeric_Shunyi = dataframes["Shunyi"].select_dtypes(exclude=['number'])

numeric_Tiantan = dataframes["Tiantan"].select_dtypes(include=['number'])
non_numeric_Tiantan = dataframes["Tiantan"].select_dtypes(exclude=['number'])

numeric_Wanliu = dataframes["Wanliu"].select_dtypes(include=['number'])
non_numeric_Wanliu = dataframes["Wanliu"].select_dtypes(exclude=['number'])

numeric_Wanshouxigong = dataframes["Wanshouxigong"].select_dtypes(include=['number'])
non_numeric_Wanshouxigong = dataframes["Wanshouxigong"].select_dtypes(exclude=['number'])


# %%
"""
Imputasi untuk kolom numerik
"""

# %%
datasets = [
    numeric_Aotizhongxin, numeric_Changping, numeric_Dingling,
    numeric_Dongsi, numeric_Guanyuan, numeric_Gucheng,
    numeric_Huairou, numeric_Nongzhanguan, numeric_Shunyi,
    numeric_Tiantan, numeric_Wanliu, numeric_Wanshouxigong
]

# Mengisi nilai yang hilang dengan rata-rata kolom numerik
for data in datasets:
    data.fillna(data.mean(numeric_only=True), inplace=True)


# %%
"""
Imputasi untuk kolom non-numerik
"""

# %%
for column_data in [
    non_numeric_Aotizhongxin, non_numeric_Changping, non_numeric_Dingling,
    non_numeric_Dongsi, non_numeric_Guanyuan, non_numeric_Gucheng,
    non_numeric_Huairou, non_numeric_Nongzhanguan, non_numeric_Shunyi,
    non_numeric_Tiantan, non_numeric_Wanliu, non_numeric_Wanshouxigong
]:
    column_data.fillna(column_data.mode().iloc[0], inplace=True)


# %%
"""
Gabungkan kembali kolom numerik dan non-numerik
"""

# %%
df_Aotizhongxin_final = pd.concat([numeric_Aotizhongxin, non_numeric_Aotizhongxin], axis=1)
df_Changping_final = pd.concat([numeric_Changping, non_numeric_Changping], axis=1)
df_Dingling_final = pd.concat([numeric_Dingling, non_numeric_Dingling], axis=1)
df_Dongsi_final = pd.concat([numeric_Dongsi, non_numeric_Dongsi], axis=1)
df_Guanyuan_final = pd.concat([numeric_Guanyuan, non_numeric_Guanyuan], axis=1)
df_Gucheng_final = pd.concat([numeric_Gucheng, non_numeric_Gucheng], axis=1)
df_Huairou_final = pd.concat([numeric_Huairou, non_numeric_Huairou], axis=1)
df_Nongzhanguan_final = pd.concat([numeric_Nongzhanguan, non_numeric_Nongzhanguan], axis=1)
df_Shunyi_final = pd.concat([numeric_Shunyi, non_numeric_Shunyi], axis=1)
df_Tiantan_final = pd.concat([numeric_Tiantan, non_numeric_Tiantan], axis=1)
df_Wanliu_final = pd.concat([numeric_Wanliu, non_numeric_Wanliu], axis=1)
df_Wanshouxigong_final = pd.concat([numeric_Wanshouxigong, non_numeric_Wanshouxigong], axis=1)


# %%
"""
Cek nilai yang hilang setelah imputasi
"""

# %%
dataframes = {
    "Aotizhongxin": df_Aotizhongxin_final,
    "Changping": df_Changping_final,
    "Dingling": df_Dingling_final,
    "Dongsi": df_Dongsi_final,
    "Guanyuan": df_Guanyuan_final,
    "Gucheng": df_Gucheng_final,
    "Huairou": df_Huairou_final,
    "Nongzhanguan": df_Nongzhanguan_final,
    "Shunyi": df_Shunyi_final,
    "Tiantan": df_Tiantan_final,
    "Wanliu": df_Wanliu_final,
    "Wanshouxigong": df_Wanshouxigong_final
}

for name, df in dataframes.items():
    missing_values = df.isnull().sum()
    print(f"Jumlah data yang hilang di {name}:\n{missing_values}\n")


# %%
"""
Winsorization untuk mengatasi outlier
"""

# %%
def winsorize_dataframe(dataframe, lower=0.05, upper=0.95):
    modified_df = dataframe.copy()
    for col in modified_df.select_dtypes(include=['number']).columns:
        low_threshold = modified_df[col].quantile(lower)
        high_threshold = modified_df[col].quantile(upper)
        modified_df[col] = modified_df[col].clip(lower=low_threshold, upper=high_threshold)
    return modified_df

# List of DataFrames for each station
stations = [df_Aotizhongxin, df_Changping, df_Dingling, df_Dongsi, df_Guanyuan,
            df_Gucheng, df_Huairou, df_Nongzhanguan, df_Shunyi, df_Tiantan,
            df_Wanliu, df_Wanshouxigong]

# Apply Winsorization to all DataFrames
winsorized_stations = {f"winsorized_{i}": winsorize_dataframe(station) for i, station in enumerate(stations)}


# %%
for name, df in winsorized_stations.items():
    print(f"Summary of {name}:")
    print(df.describe())


# %%
"""
Boxplots setelah winsorized untuk mengecek apakah masih ada outlier
"""

# %%
import matplotlib.pyplot as plt
import seaborn as sns

def visualize_winsorized_boxplots(dataframe, location_name, fig_size=(14, 8)):
    """
    Menampilkan boxplot untuk data setelah proses Winsorizing.
    """
    plt.figure(figsize=fig_size)
    sns.boxplot(data=dataframe, orient='h', palette="Set2")
    plt.title(f'Winsorized Boxplot - {location_name}', fontsize=14)
    plt.xlabel('Value')
    plt.ylabel('Features')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()

# Loop over the winsorized stations to generate the boxplots
for name, df in winsorized_stations.items():
    location_name = f"Station {name.split('_')[1]}"  # Get station name from the dictionary key
    visualize_winsorized_boxplots(df, location_name)


# %%
"""
Fixed data type
"""

# %%
dataframes = [
    df_Aotizhongxin, df_Changping, df_Dingling, df_Dongsi,
    df_Guanyuan, df_Gucheng, df_Huairou, df_Nongzhanguan,
    df_Shunyi, df_Tiantan, df_Wanliu, df_Wanshouxigong
]

df_names = [
    "df_Aotizhongxin", "df_Changping", "df_Dingling", "df_Dongsi",
    "df_Guanyuan", "df_Gucheng", "df_Huairou", "df_Nongzhanguan",
    "df_Shunyi", "df_Tiantan", "df_Wanliu", "df_Wanshouxigong"
]

for df in dataframes:
    df["date_time"] = pd.to_datetime(df.loc[:, ["year", "month", "day", "hour"]])

for name, df in zip(df_names, dataframes):
    print(f"{name} data types:\n", df.dtypes, "\n")


# %%
"""
## Exploratory Data Analysis (EDA)
"""

# %%
"""
Gabungkan data
"""

# %%
import pandas as pd

# Menggabungkan beberapa DataFrame menjadi satu
dataframes = [df_Aotizhongxin, df_Changping, df_Dingling, df_Dongsi,
              df_Guanyuan, df_Gucheng, df_Huairou, df_Nongzhanguan,
              df_Shunyi, df_Tiantan, df_Wanliu, df_Wanshouxigong]

df_combined = pd.concat(dataframes, ignore_index=True)


# %%
"""
Mengonversi kolom date_time ke tipe datetime
"""

# %%
# Assuming you already have your individual DataFrames (e.g., df_Aotizhongxin, df_Changping, etc.)
df_all = pd.concat([df_Aotizhongxin, df_Changping, df_Dingling, df_Dongsi, df_Guanyuan,
                    df_Gucheng, df_Huairou, df_Nongzhanguan, df_Shunyi, df_Tiantan,
                    df_Wanliu, df_Wanshouxigong], ignore_index=True)
df_all['date_time'] = pd.to_datetime(df_all.loc[:, ['year', 'month', 'day', 'hour']])
print(df_all.columns)


# %%
"""
Analisis Deskriptif
"""

# %%
print(df_all.describe())

# %%
"""
Cek missing value
"""

# %%
print(df_all.isnull().sum())

# %%
"""
Drop missing value
"""

# %%
df_all= df_all.dropna()


# %%
"""
Mendeteksi dan menghitung baris dengan index duplikat
"""

# %%
print(df_all.index.duplicated().sum())


# %%
"""
Mendeteksi dan menampilkan kolom duplikat
"""

# %%
print(df_all.columns[df_all.columns.duplicated()])


# %%
df_all = df_all.loc[:, ~df_all.columns.duplicated()]


# %%
df_all.to_csv('clean_df_all.csv', index=False)


# %%
"""
Hubungan Angin dengan Persebaran PM2.5
"""

# %%
plt.figure(figsize=(9, 5))
sns.scatterplot(data=df_all, x='WSPM', y='PM2.5', alpha=0.7, color='blue')
plt.xlabel('Wind Speed (WSPM)')
plt.ylabel('PM2.5 Concentration')
plt.title('Wind Speed vs PM2.5 Scatter Plot')
plt.grid(True)
plt.show()

# %%
"""
Korelasi antara variabel
"""

# %%
# Menghitung matriks korelasi untuk fitur tertentu
selected_features = ['PM2.5', 'WSPM', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
korelasi_matrix = df_all[selected_features].corr()

# Plot heatmap
plt.figure(figsize=(9, 5))
sns.heatmap(korelasi_matrix, annot=True, cmap='RdBu_r', linewidths=0.5)
plt.title('Peta Korelasi Variabel')
plt.show()


# %%
"""
Konsentrasi Polutan dari Kendaraan Bermotor atau bahan bakar fosil (CO & NO2)
"""

# %%
# Resampling data per bulan dan menghitung rata-rata
df_grouped = df_all.set_index('date_time')[['CO', 'NO2']].resample('M').mean().reset_index()

# Membuat visualisasi
plt.figure(figsize=(10, 5))
sns.lineplot(data=df_grouped, x='date_time', y='CO', label='CO', marker='o')
sns.lineplot(data=df_grouped, x='date_time', y='NO2', label='NO2', marker='s')

plt.xlabel('Waktu')
plt.ylabel('Konsentrasi')
plt.title('Tren Bulanan Konsentrasi CO dan NO2')
plt.legend()
plt.grid(True)
plt.show()

# %%
"""
Kaitan Hujan dengan Tingkat Polutan
"""

# %%

df_all = df_all.reset_index(drop=True)
plt.figure(figsize=(30, 6))
sns.boxplot(x='RAIN', y='PM2.5', data=df_all)
plt.title('Pengaruh Hujan terhadap PM2.5')
plt.xlabel('Hujan (RAIN)', labelpad=20)
plt.ylabel('Konsentrasi PM2.5')


plt.xticks(rotation=45, ha='right')

plt.show()




# %%
"""
Kaitan Polutan NO2 dan CO dengan O3
"""

# %%
plt.figure(figsize=(10, 6))
sns.scatterplot(x='NO2', y='O3', data=df_all)
plt.title('Scatterplot of NO2 vs O3')
plt.show()

# %%
plt.figure(figsize=(9, 5))
sns.scatterplot(data=df_all, x='CO', y='O3', alpha=0.8)
plt.title('Hubungan antara CO dan O3')
plt.xlabel('Konsentrasi CO')
plt.ylabel('Konsentrasi O3')
plt.grid(True)
plt.show()


# %%
plt.figure(figsize=(10, 6))
sns.scatterplot(x='CO', y='O3', data=df_all)
plt.title('Scatterplot of CO vs O3')
plt.show()

# %%
"""
Correlation Heatmap khusus O3 dengan polutan lain
"""

# %%
corr_matrix = df_all.loc[:, ['O3', 'PM2.5', 'PM10', 'SO2', 'NO2', 'CO']].corr()
plt.figure(figsize=(9, 5))
sns.heatmap(corr_matrix, annot=True, cmap='RdBu_r', fmt=".2f", linewidths=0.5)
plt.title('Korelasi O3 dengan Polutan Lainnya')
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.show()


# %%
"""
## Visualization & Explanatory Analysis
"""

# %%
"""
### Pertanyaan 1: Seberapa besar dampak kecepatan angin (WSPM) terhadap distribusi konsentrasi PM2.5 selama periode musim kemarau (Juni–Agustus)?
"""

# %%
df_all['bulan'] = df_all['date_time'].dt.month

kemarau = df_all[df_all['bulan'].between(6, 8)]

plt.figure(figsize=(12, 6))
sns.scatterplot(data=kemarau, x='WSPM', y='PM2.5', alpha=0.7)
plt.title('Korelasi Kecepatan Angin terhadap PM2.5 di Musim Kemarau')
plt.xlabel('Kecepatan Angin (WSPM)')
plt.ylabel('Kadar PM2.5')
plt.grid(True)
plt.show()

# %%
dry_season_data = df_all[df_all['month'].isin([6, 7, 8])]

monthly_avg = dry_season_data.groupby(['year', 'month']).agg({'WSPM': 'mean', 'PM2.5': 'mean'}).reset_index()

plt.figure(figsize=(12, 6))
sns.lineplot(x='WSPM', y='PM2.5', hue='month', data=dry_season_data, marker='o', palette='coolwarm')
plt.title('Hubungan Kecepatan Angin (WSPM) dengan PM2.5 Selama Musim Kemarau (Juni hingga Agustus)')
plt.xlabel('Kecepatan Angin (WSPM)')
plt.ylabel('Konsentrasi PM2.5')
plt.legend(title='Bulan', labels=['Juni', 'Juli', 'Agustus'])
plt.show()


# %%
"""
### Pertanyaan 2: Bagaimana dampak konsentrasi NO2 dan CO sebagai polutan dari kendaraan bermotor terhadap kualitas udara?
"""

# %%
df_all['month_year'] = df_all['date_time'].dt.to_period('M')

data_monthly = df_all.groupby('month_year')[['CO', 'NO2', 'PM2.5', 'PM10', 'SO2', 'O3']].mean().reset_index()

data_monthly['month_year'] = data_monthly['month_year'].dt.to_timestamp()

plt.figure(figsize=(14, 8))
colors = ['blue', 'red', 'green', 'purple', 'orange', 'cyan']
labels = ['CO', 'NO2', 'PM2.5', 'PM10', 'SO2', 'O3']

for col, color in zip(labels, colors):
    sns.lineplot(x='month_year', y=col, data=data_monthly, label=col, color=color)

plt.title('Tren Bulanan Konsentrasi Polutan')
plt.xlabel('Waktu (Bulan)')
plt.ylabel('Rata-rata Konsentrasi')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# %%
"""
### Pertanyaan 3: Bagaimana dampak hujan terhadap zat pencemar yang menyebabkan polusi udara?
"""

# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Kategorisasi hujan berdasarkan intensitas
df_all['RAIN_CATEGORY'] = pd.cut(df_all['RAIN'], bins=[0, 1, 4, 8, 10],
                                 labels=['No Rain', 'Light Rain', 'Moderate Rain', 'Heavy Rain'])

# Plot boxplot untuk melihat distribusi PM2.5 berdasarkan kategori hujan
plt.figure(figsize=(12, 6))
sns.boxplot(x='RAIN_CATEGORY', y='PM2.5', data=df_all)
plt.title('Distribution of PM2.5 Levels by Rain Intensity')
plt.xlabel('Rain Intensity Category')
plt.ylabel('PM2.5 Concentration')
plt.xticks(rotation=30)
plt.grid(True, linestyle='--', alpha=0.7)

plt.show()

# %%
df_all['RAIN_GROUP'] = pd.cut(df_all['RAIN'], bins=[0, 1, 4, 8, 10], labels=['No Rain', 'Light Rain', 'Moderate Rain', 'Heavy Rain'])

rain_group_avg = df_all.groupby('RAIN_GROUP')['PM2.5'].mean().reset_index()

plt.figure(figsize=(12, 6))
sns.lineplot(x='RAIN_GROUP', y='PM2.5', data=rain_group_avg, marker='o', color='blue')

plt.title('Rata-rata Konsentrasi PM2.5 Berdasarkan Intensitas Hujan')
plt.xlabel('Kelompok Intensitas Hujan')
plt.ylabel('Rata-rata Konsentrasi PM2.5')

plt.show()


# %%
"""
### Pertanyaan 4: Bagaimana keterkaitan antara kadar NO₂ dan CO dengan proses pembentukan O₃?
"""

# %%
df_all['month_period'] = df_all['date_time'].dt.to_period('M')

avg_monthly = df_all.groupby('month_period')[['NO2', 'CO', 'O3']].mean().reset_index()

avg_monthly['month_period'] = avg_monthly['month_period'].dt.to_timestamp()

plt.figure(figsize=(12, 6))

sns.lineplot(data=avg_monthly, x='month_period', y='NO2', label='NO2', color='crimson')
sns.lineplot(data=avg_monthly, x='month_period', y='CO', label='CO', color='navy')
sns.lineplot(data=avg_monthly, x='month_period', y='O3', label='O3', color='forestgreen')

plt.title('Tren Bulanan Konsentrasi NO2, CO, dan O3')
plt.xlabel('Waktu (Bulan)')
plt.ylabel('Rata-rata Konsentrasi Polutan')
plt.legend()

plt.xticks(rotation=45)
plt.grid(which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()

# %%
corr_matrix = df_all[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'WSPM', 'TEMP', 'RAIN']].corr()
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Heatmap Korelasi Antara Variabel Polutan dan Faktor Lingkungan')
plt.show()


# %%
"""
## Conclusion
"""

# %%
"""
Dari hasil analisis, dapat disimpulkan bahwa:

1. Kecepatan angin (WSPM) memiliki peran penting dalam penyebaran polutan. Ketika angin bertiup kencang, konsentrasi PM2.5 cenderung berkurang karena polutan menyebar lebih luas, menciptakan tren negatif antara kecepatan angin dan kadar PM2.5. Namun, dalam kondisi angin sedang, polutan dapat terkumpul di suatu area, sehingga konsentrasinya justru meningkat.

2. Kenaikan kadar CO dan NO₂ seringkali mengindikasikan peningkatan aktivitas kendaraan bermotor atau pembakaran bahan bakar fosil. Ini menunjukkan bahwa kendaraan dan bahan bakar fosil memiliki kontribusi signifikan dalam pencemaran udara.

3. Hujan dapat membantu mengurangi kadar polutan, termasuk PM2.5, karena polutan terbawa turun bersama air hujan, sehingga menyebabkan penurunan konsentrasi polutan. Namun, dalam kasus hujan deras, PM2.5 dapat meningkat akibat pengadukan partikel dari tanah atau reaksi lainnya.

4. Konsentrasi NO₂ dan CO berpengaruh terhadap pembentukan O3. Ketika kadar NO₂ meningkat, kadar O3 akan cenderung turun, dan sebaliknya. NO₂ dapat berperan dalam reaksi yang mengurangi O3 di atmosfer. Di lingkungan dengan CO yang tinggi, pembentukan O3 bisa melambat karena reaksi kimia yang terjadi.

"""
