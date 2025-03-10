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

# Navigasi Sidebar
st.sidebar.title("Navigasi")
menu = st.sidebar.radio("Pilih Menu", ["Beranda", "Indeks UV", "Data UV", "Grafik"])

# Tampilan Beranda
if menu == "Beranda":
    st.markdown("<h1 style='text-align: center; color: purple;'>🌞 Sistem Pemantauan Radiasi UV</h1>", unsafe_allow_html=True)
    st.write("Selamat datang di sistem pemantauan radiasi UV! Pantau indeks UV secara real-time dan analisis historisnya.")

# Tampilan gauge chart
elif menu == "Indeks UV":
latest_data = data.iloc[-1] 
latest_time = latest_data.name 
uv_index = latest_data['Index'] 

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=uv_index,
    gauge={
        'axis': {'range': [0, 11]},
        'bar': {'color': "#3098ff"},
        'steps': [
            {'range': [0, 3], 'color': "#00ff00"},
            {'range': [3, 6], 'color': "#ffff00"},
            {'range': [6, 8], 'color': "#ff6600"},
            {'range': [8, 10], 'color': "#ff0000"},
            {'range': [10,11], 'color': "#9900cc"},
        ]
    }
))

fig.update_layout(
    margin=dict(t=30, b=30, l=30, r=30),
)

st.plotly_chart(fig, use_container_width=True)
st.markdown(
    f"""
    <div style="text-align: center;">
        <span style="display: inline-block; padding: 5px 15px; border-radius: 5px;
                    background-color: {'#d4edda' if uv_index <= 2 else '#fcfac0' if uv_index <= 5 else '#ffc78f' if uv_index <= 7 else '#ff8a8a' if uv_index <= 10 else '#e7cafc'};">
            {"<p style='color: #00ff00;'><strong>✅ Tingkat aman:</strong> Gunakan pelembab tabir surya SPF 30+ dan kacamata hitam.</p>" if uv_index <= 2 else
             "<p style='color: #ffcc00;'><strong>⚠️ Tingkat bahaya sedang:</strong> Oleskan cairan pelembab tabir surya SPF 30+ setiap 2 jam, kenakan pakaian pelindung matahari.</p>" if uv_index <= 5 else
             "<p style='color: #ff6600;'><strong>⚠️ Tingkat bahaya tinggi:</strong> Kurangi paparan matahari antara pukul 10 pagi hingga pukul 4 sore.</p>" if uv_index <= 7 else
             "<p style='color: #ff0000;'><strong>⚠️ Tingkat bahaya sangat tinggi:</strong> Tetap di tempat teduh dan oleskan sunscreen setiap 2 jam.</p>" if uv_index <= 10 else
             "<p style='color: #9900cc;'><strong>❗ Tingkat bahaya ekstrem:</strong> Diperlukan semua tindakan pencegahan karena kulit dan mata dapat rusak dalam hitungan menit.</p>"}
       </span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div style="text-align: center; font-size: medium; margin-top: 10px; margin-bottom: 40px;">
        <p><b>Pukul:</b> {latest_time.strftime('%H:%M')}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Tampilan Data UV
elif menu == "Data UV":
    st.subheader("📊 Data Historis Indeks UV")
    st.write("Data dari Google Sheets:", data)

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
