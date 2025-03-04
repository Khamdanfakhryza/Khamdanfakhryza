# Belajar Analisis Data dengan Python

## Dataset: Air Quality

[Air Quality Dataset](https://github.com/marceloreis/HTI/tree/master)

## Streamlit Cloud :

![dampak](https://github.com/user-attachments/assets/1d9df9f6-0d1d-4080-9883-6bc4ebd5d998)

Streamlit Cloud : (https://khamdanfakhryza.streamlit.app/)

## Setup environment

- Install Visual Studio Code for Editor
- Execute this command on command line (as administrator preferred)

```
pip install numpy pandas scipy matplotlib seaborn jupyter streamlit
```

## Project installation

The steps to create your virtual environment from this project is as follows:

1. Clone this repository
   ```
   git clone https://github.com/Khamdanfakhryza/Khamdanfakhryza.git
   ```

2. Move to directory dicoding-airquality/
   ```
   cd Khamdanfakhryza
   ```
3. Run streamlit app
   ```
   streamlit run dashboard.py
   ```
4. Stop the application program by `ctrl + c`.

---

## Panduan Eksplorasi Data (EDA) dan Analisis

Pada tahapan **Exploratory Data Analysis (EDA)**, kita melakukan **aggregasi data** untuk mengenal dataset lebih dalam sebelum visualisasi. Langkah-langkah yang dilakukan:

1. **Validasi Data**: Memastikan semua file dataset tersedia dan tidak korup.
2. **Pembersihan Data**: Menghapus data yang hilang atau duplikat.
3. **Transformasi Waktu**: Menggabungkan tahun, bulan, hari, dan jam ke dalam satu kolom `date_time`.
4. **Agregasi Data**:
   - Melihat tren polutan berdasarkan waktu (harian, bulanan, tahunan).
   - Mengelompokkan data berdasarkan musim untuk analisis pola musiman.
   - Menghitung rata-rata PM2.5 berdasarkan kecepatan angin dan curah hujan.

Pada tahapan **kesimpulan**, kita fokus pada hasil analisis data dengan menyebutkan nilai ekstrem (tertinggi/terendah) dan pola signifikan yang ditemukan, seperti:

- **Dampak Kecepatan Angin**: Angin lebih dari 5 m/s menurunkan PM2.5 hingga 40%.
- **Efek Curah Hujan**: Hujan deras (>7.6mm) mampu menurunkan polusi udara hingga 55%.
- **Pola Musiman**: PM2.5 tertinggi di musim dingin dan terendah di musim panas.

Selain kesimpulan, rekomendasi juga bisa diberikan berdasarkan hasil analisis untuk mitigasi polusi udara.

---

**Thank youuu!!**

