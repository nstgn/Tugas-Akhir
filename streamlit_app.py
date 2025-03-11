import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from streamlit_gsheets import GSheetsConnection
import plotly.graph_objects as go

# Koneksi ke Google Sheets
url = "https://docs.google.com/spreadsheets/d/1SczaIV1JHUSca1hPilByJFFzOi5a8Hkhi0OemlmPQsY/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)
data = conn.read(spreadsheet=url, usecols=[0, 1, 2, 3], ttl=0)

# Pastikan data tidak kosong
if data is not None and not data.empty:
    data.columns = ["Date", "Time", "Intensity", "Index"]
    data["Waktu"] = pd.to_datetime(data["Date"] + " " + data["Time"])
    data = data.sort_values(by="Waktu")

# Custom Header
st.markdown(
    """
    <style>
    .header {
        background-color: #D6D6F5; padding: 10px; text-align: center; border-radius: 7px;
    }
    .header img {
        width: 60px;
    }
    </style>
    <div class="header">
        <img src="https://upload.wikimedia.org/wikipedia/id/2/2d/Undip.png" alt="Logo">
    </div>
    """,
    unsafe_allow_html=True
)

# Navigasi Sidebar
st.sidebar.title("Navigasi")
menu = st.sidebar.radio("Pilih Menu", ["Beranda", "Indeks UV", "Panduan Perlindungan", "Data Historis"])

# Tampilan Beranda
if menu == "Beranda":
    st.markdown(""" 
    <h1 style='text-align: center; color: #6a0dad;'> SISTEM PREDIKSI INDEKS UV</h1>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="max-width: 600px; margin: auto; text-align: left;">
        <p style="font-size: 18px; font-weight: bold; margin-bottom: 5px;">Selamat datang❕</p>
        <p style="text-align: justify;">
            Sistem ini menggunakan data dari sensor ML8511 untuk memprediksi indeks UV dengan model 
            Long Short-Term Memory (LSTM). Prediksi ini membantu dalam memahami pola paparan UV serta 
            tindakan pencegahan yang diperlukan berdasarkan estimasi indeks UV dalam beberapa jam ke depan.
        </p>
    </div>
    """, unsafe_allow_html=True)

elif menu == "Indeks UV":
    st.subheader("🌞 Kondisi UV Sekarang")

elif menu == "Panduan Perlindungan":
    st.subheader("🛡️ Panduan Perlindungan")

elif menu == "Data Historis":
    st.subheader("📊 Data Historis Indeks UV")

# Custom Footer
st.markdown(
    """
    <style>
    .footer {
        position: fixed; bottom: 0; right: 70px; font-size: 12px; text-align: left; margin: 0; padding: 5px 10px;
    }
    </style>
    <div class="footer">
        <p>Universitas Diponegoro<br>Fakultas Sains dan Matematika<br>Departemen Fisika</p>
        <p>Nastangini<br>20440102130112</p>
    </div>
    """, unsafe_allow_html=True)
