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
menu = st.sidebar.radio("Pilih Menu", ["Beranda", "Indeks UV", "Data Historis"])

# Tampilan Beranda
if menu == "Beranda":
    st.markdown("<h1 style='text-align: center; color: purple;'>🌞 Sistem Pemantauan Radiasi UV</h1>", unsafe_allow_html=True)
    st.write("Selamat datang di sistem pemantauan radiasi UV! Pantau indeks UV secara real-time dan analisis historisnya.")

# Tampilan Indeks UV (Gauge Chart)
elif menu == "Indeks UV":
        last_index = data['Index'].iloc[-1]
        last_time = data['Waktu'].iloc[-1].time()
        st.write(last_time)
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=last_index,
            gauge={
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

        fig.update_layout(margin=dict(t=30, b=30, l=30, r=30))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            f"""
            <div style="text-align: center;">
                <span style="display: inline-block; padding: 5px 15px; border-radius: 5px;
                            background-color: {'#d4edda' if last_index <= 2 else '#fcfac0' if last_index <= 5 else '#ffc78f' if last_index <= 7 else '#ff8a8a' if last_index <= 10 else '#e7cafc'};">
                    {"✅ Tingkat aman: Gunakan sunscreen SPF 30+." if last_index <= 2 else
                     "⚠️ Bahaya sedang: Oleskan sunscreen setiap 2 jam." if last_index <= 5 else
                     "⚠️ Bahaya tinggi: Hindari paparan langsung saat siang." if last_index <= 7 else
                     "⚠️ Bahaya sangat tinggi: Gunakan pakaian pelindung & topi." if last_index <= 10 else
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

elif menu == "Data Historis":
    if data is not None and not data.empty:
        st.subheader("📊 Data Historis Indeks UV")

        # Membuat dua kolom: kiri (tabel) & kanan (grafik)
        col1, col2 = st.columns([1, 2])  # Kolom kiri lebih kecil dari kanan

        with col1:
            st.write("📋 **Tabel Data**")
            st.dataframe(data.tail(20), height=400)  # Menampilkan 20 data terbaru

        with col2:
            st.write("📈 **Grafik Indeks UV**")
            fig = px.line(
                data, 
                x=data.index, 
                y="Index", 
                markers=True, 
                title="Grafik Indeks UV Seiring Waktu",
                labels={"Index": "Indeks UV", "index": "Waktu"}
            )
            fig.update_traces(line=dict(color="purple"), fill="tozeroy")  # Warna & area fill
            fig.update_layout(xaxis=dict(rangeslider=dict(visible=True)))  # Scroll horizontal

            st.plotly_chart(fig, use_container_width=True)  # Grafik responsif
    else:
        st.warning("Data tidak tersedia.")

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
