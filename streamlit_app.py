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
menu = st.sidebar.radio("Pilih Menu", ["Beranda", "Indeks UV", "abel Proteksi", "Data Historis"])

# Tampilan Beranda
if menu == "Beranda":
    st.markdown(""" 
    <h1 style='text-align: center; color: #6a0dad;'>🌞 SISTEM PREDIKSI INDEKS UV</h1>
    """, unsafe_allow_html=True)
    
    st.write("""
    Selamat datang❕
    Sistem ini menggunakan data dari sensor ML8511 untuk memprediksi indeks UV dengan model 
    Long Short-Term Memory (LSTM). Prediksi ini membantu dalam memahami pola paparan UV serta tindakan pencegahan 
    yang diperlukan berdasarkan estimasi indeks UV dalam beberapa jam ke depan.
    """)

elif menu == "Indeks UV":
    last_index = data['Index'].iloc[-1]
    last_time = data['Waktu'].iloc[-1].time()
        
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=last_index, gauge={
            'axis': {'range': [0, 11]},
            'bar': {'color': "#3098ff"},
            'steps': [
                {'range': [0, 3], 'color': "#00ff00"},
                {'range': [3, 6], 'color': "#ffff00"},
                {'range': [6, 8], 'color': "#ff6600"},
                {'range': [8, 10], 'color': "#ff0000"},
                {'range': [10, 11], 'color': "#9900cc"},
            ]
        }
    ))
    fig.update_layout(
        margin=dict(t=30, b=30, l=30, r=30)
        height=250, width=400,)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
            f"""
            <div style="text-align: center;">
                <span style="display: inline-block; padding: 5px 15px; border-radius: 5px;
                            background-color: {'#d4edda' if last_index <= 2 else '#fcfac0' if last_index <= 5 else '#ffc78f' if last_index <= 7 else '#ff8a8a' if last_index <= 10 else '#e7cafc'};">
                    {"✅ Tingkat aman: Gunakan sunscreen SPF 30+." if last_index <= 2 else
                     "⚠️ Bahaya sedang: Oleskan sunscreen setiap 2 jam, kenakan pakaian pelindung matahari." if last_index <= 5 else
                     "⚠️ Bahaya tinggi: Hindari paparan langsung saat siang." if last_index <= 7 else
                     "⚠️ Bahaya sangat tinggi:Tetap di tempat teduh, gunakan pakaian pelindung & topi." if last_index <= 10 else
                     "❗ Bahaya ekstrem: Kurangi aktivitas luar ruangan!"}
               </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div style="text-align: center; font-size: medium; margin-top: 10px; margin-bottom: 40px;">
                <p><b>Pukul:</b> {last_time.strftime('%H:%M')}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

elif menu == "Tabel Proteksi":
    st.write("Tabel Proteksi")

elif menu == "Data Historis":
    st.write("Halaman Data Historis")

# Custom Footer
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        right: 70px;
        font-size: 12px;
        text-align: left;
        margin: 0;
        padding: 5px 10px;
    }
    </style>
    <div class="footer">
        <p>Universitas Diponegoro<br>Fakultas Sains dan Matematika<br>Departemen Fisika</p>
        <p>Nastangini<br>20440102130112</p>
    </div>
    """,
    unsafe_allow_html=True
)
