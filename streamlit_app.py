import numpy as np
import pandas as pd
import streamlit as st
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

#14 Tampilan
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

st.markdown(
    """
    <h1 style="text-align: center;">UV Index</h1>
    """,
    unsafe_allow_html=True,
)

# Navigasi Sidebar
st.sidebar.title("Navigasi")
menu = st.sidebar.radio("Pilih Menu", ["Beranda", "Data UV", "Grafik"])

# Tampilan Beranda
if menu == "Beranda":
    st.markdown("<h1 style='text-align: center; color: purple;'>🌞 Sistem Pemantauan Radiasi UV</h1>", unsafe_allow_html=True)
    st.write("Selamat datang di sistem pemantauan radiasi UV! Pantau indeks UV secara real-time dan analisis historisnya.")

# Tampilan Data UV
elif menu == "Data UV":
    st.subheader("📊 Data Historis Indeks UV")
    
    # Pewarnaan DataFrame untuk Indeks UV
    def highlight_uv(val):
        if val < 3:
            color = "green"
        elif val < 6:
            color = "yellow"
        elif val < 8:
            color = "orange"
        else:
            color = "red"
        return f"background-color: {color}; color: white;"

    styled_data = data.style.applymap(highlight_uv, subset=["Indeks UV"])
    st.dataframe(styled_data)

# Tampilan Grafik
elif menu == "Grafik":
    st.subheader("📈 Visualisasi Data Indeks UV")

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(data["Waktu"], data["Indeks UV"], marker="o", linestyle="-", color="purple", label="Indeks UV")
    ax.fill_between(data["Waktu"], data["Indeks UV"], color="purple", alpha=0.3)
    ax.set_xlabel("Waktu")
    ax.set_ylabel("Indeks UV")
    ax.set_title("Grafik Indeks UV Seiring Waktu")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

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
