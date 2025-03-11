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

# 2 Pre-Processing
if data is not None and not data.empty:
    data.columns = ["Date", "Time", "Intensity", "Index"]
    data["Waktu"] = pd.to_datetime(data["Date"] + " " + data["Time"])
    data = data.sort_values(by="Waktu")
    data.set_index('Waktu', inplace=True)
    data = data[['Index']].copy()
    last_index = data['Index'].iloc[-1]
    last_time = data.index[-1]
    data = data.between_time('06:00', '18:05')
    date_range = pd.date_range(start=data.index.min(), end=data.index.max(), freq='2min')
    data = data.reindex(date_range)
    data['Index'].interpolate(method='linear', inplace=True)

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
    <h1 style='text-align: center; color: #6a0dad; font-size: 32px; font-weight: bold;'> 
        SISTEM PREDIKSI INDEKS UV 
    </h1>
    <hr style='border: 2px solid #6a0dad; width: 50%; margin: auto;'>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="max-width: 650px; margin: auto; text-align: justify; padding: 20px; background-color: #f9f9f9; 
                border-radius: 10px; box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);">
        <h2 style="text-align: center; color: #6a0dad; font-size: 24px; font-weight: bold; margin-bottom: 10px;">
            Selamat Datang!
        </h2>
        <p style="font-size: 16px; line-height: 1.6; color: #333;">
            Sistem ini menggunakan data dari sensor <b>ML8511</b> untuk memprediksi indeks UV dengan model 
            <b>Long Short-Term Memory (LSTM)</b>. Prediksi ini bertujuan untuk memahami pola paparan UV serta 
            memberikan informasi yang mendukung tindakan pencegahan secara lebih akurat dan efisien. 
            Dengan estimasi indeks UV dalam beberapa jam ke depan, sistem ini membantu meningkatkan kewaspadaan 
            terhadap risiko paparan radiasi UV yang berlebihan.
        </p>
    </div>
    """, unsafe_allow_html=True)


elif menu == "Indeks UV":
    st.subheader("🌞 Kondisi UV Sekarang")
    last_index = data['Index'].iloc[-1]
    last_time = data.index[-1].time()
        
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
        margin=dict(t=30, b=30, l=30, r=30))
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"""
    <div style="text-align: center;"><span style="display: inline-block; padding: 5px 15px; border-radius: 5px;
                    background-color: {'#d4edda' if last_index <= 2 else '#fcfac0' if last_index <= 5 else '#ffc78f' if last_index <= 7 else '#ff8a8a' if last_index <= 10 else '#e7cafc'};">
            {"<p style='color: #00ff00;'><strong>✅ Tingkat aman:</strong> Gunakan pelembab tabir surya SPF 30+ dan kacamata hitam.</p>" if last_index <= 2 else
             "<p style='color: #ffcc00;'><strong>⚠️ Tingkat bahaya sedang:</strong> Oleskan cairan pelembab tabir surya SPF 30+ setiap 2 jam, kenakan pakaian pelindung matahari.</p>" if last_index <= 5 else
             "<p style='color: #ff6600;'><strong>⚠️ Tingkat bahaya tinggi:</strong> Kurangi paparan matahari antara pukul 10 pagi hingga pukul 4 sore.</p>" if last_index <= 7 else
             "<p style='color: #ff0000;'><strong>⚠️ Tingkat bahaya sangat tinggi:</strong> Tetap di tempat teduh dan oleskan sunscreen setiap 2 jam.</p>" if last_index <= 10 else
             "<p style='color: #9900cc;'><strong>❗ Tingkat bahaya ekstrem:</strong> Diperlukan semua tindakan pencegahan karena kulit dan mata dapat rusak dalam hitungan menit.</p>"}
       </span>
    </div>
    """, unsafe_allow_html=True,)
    
    st.markdown(f"""
    <div style="text-align: center; font-size: medium; margin-top: 10px; margin-bottom: 40px;">
        <p><b>Pukul:</b> {last_time.strftime('%H:%M')}</p>
    </div>
    """,unsafe_allow_html=True,)
    
    st.subheader("⏳ Prediksi Indeks UV")
    cols = st.columns(len(future_df))
    for i, row in future_df.iterrows():
        with cols[i]:
            uv_level = row["Predicted Index"]
            if uv_level < 3: 
                icon, desc, bg_color = "🟢", "Low", "#00ff00"
            elif uv_level < 6:
                icon, desc, bg_color = "🟡", "Moderate", "#ffe600"
            elif uv_level < 8:
                icon, desc, bg_color = "🟠", "High", "#ff8c00"
            elif uv_level < 11:
                icon, desc, bg_color = "🔴", "Very High", "#ff0000"
            else:
                icon, desc, bg_color = "🟣", "Extreme", "#9900cc"

        st.markdown(
            f"""
            <div style="text-align:center; padding:10px; border-radius:5px; background-color:{bg_color};">
                <h3 style="color:white;">{row['Time'].strftime('%H:%M')}</h3>
                <h2 style="color:white;">{icon} {uv_level}</h2>
                <p style="color:white;">{desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

elif menu == "Panduan Perlindungan":
    st.subheader("🛡️ Panduan Perlindungan")
    st.markdown("""
    <h1 style="text-align: center;margin-top: 40px; margin-bottom: 10px;">Tabel Saran Proteksi</h1>
    """,unsafe_allow_html=True,)
    
    st.markdown("""
    <table style="width:100%; border-collapse: collapse; text-align: center;">
        <tr>
            <th style="border: 1px solid black; padding: 8px;">Kategori</th>
            <th style="border: 1px solid black; padding: 8px;">Himbauan</th>
        </tr>
        <tr style="background-color: #00ff00;">
            <td style="border: 1px solid black; padding: 8px; text-align: left;">0-2 (Low)</td>
            <td style="border: 1px solid black; padding: 8px; text-align: left;">
                <ul>
                    <li>Tingkat bahaya rendah bagi orang banyak.</li>
                    <li>Kenakan kacamata hitam pada hari yang cerah.</li>
                    <li>Gunakan cairan pelembab tabir surya SPF 30+ bagi kulit sensitif.</li>
                    <li>Permukaan yang cerah, seperti pasir, air, dan salju, akan meningkatkan paparan UV.</li>
                </ul>
            </td>
        </tr>
        <tr style="background-color: #ffff00;">
            <td style="border: 1px solid black; padding: 8px; text-align: left;">3-5 (Moderate)</td>
            <td style="border: 1px solid black; padding: 8px; text-align: left;">
                <ul>
                    <li>Tingkat bahaya sedang bagi orang yang terpapar matahari tanpa pelindung.</li>
                    <li>Tetap di tempat teduh pada saat matahari terik siang hari.</li>
                    <li>Kenakan pakaian pelindung matahari, topi lebar, dan kacamata hitam yang menghalangi sinar UV, pada saat berada di luar ruangan.</li>
                    <li>Oleskan cairan pelembab tabir surya SPF 30+ setiap 2 jam bahkan pada hari berawan, setelah berenang atau berkeringat.</li>
                    <li>Permukaan yang cerah, seperti pasir, air, dan salju, akan meningkatkan paparan UV.</li>
                </ul>
            </td>
        </tr>
        <tr style="background-color: #ff6600;">
            <td style="border: 1px solid black; padding: 8px; text-align: left;">6-7 (High)</td>
            <td style="border: 1px solid black; padding: 8px; text-align: left;">
                <ul>
                    <li>Tingkat bahaya tinggi bagi orang yang terpapar matahari tanpa pelindung, diperlukan pelindung untuk menghindari kerusakan mata dan kulit.</li>
                    <li>Kurangi waktu di bawah paparan matahari antara pukul 10 pagi hingga pukul 4 sore.</li>
                    <li>Kenakan pakaian pelindung matahari, topi lebar, dan kacamata hitam yang menghalangi sinar UV, pada saat berada di luar ruangan.</li>
                    <li>Oleskan cairan pelembab tabir surya SPF 30+ setiap 2 jam bahkan pada hari berawan, setelah berenang atau berkeringat.</li>
                    <li>Permukaan yang cerah, seperti pasir, air, dan salju, akan meningkatkan paparan UV.</li>
                </ul>
            </td>
        </tr>
        <tr style="background-color: #ff0000;">
            <td style="border: 1px solid black; padding: 8px; text-align: left;">8-10 (Very High)</td>
            <td style="border: 1px solid black; padding: 8px; text-align: left;">
                <ul>
                    <li>Tingkat bahaya tinggi bagi orang yang terpapar matahari tanpa pelindung, diperlukan pelindung untuk menghindari kerusakan mata dan kulit.</li>
                    <li>Minimal waktu di bawah paparan matahari antara pukul 10 pagi hingga pukul 4 sore.</li>
                    <li>Tetap di tempat teduh pada saat matahari terik siang hari.</li>
                    <li>Kenakan pakaian pelindung matahari, topi lebar, dan kacamata hitam yang menghalangi sinar UV, pada saat berada di luar ruangan.</li>
                    <li>Oleskan cairan pelembab tabir surya SPF 30+ setiap 2 jam bahkan pada hari berawan, setelah berenang atau berkeringat.</li>
                    <li>Permukaan yang cerah, seperti pasir, air, dan salju, akan meningkatkan paparan UV.</li>
                </ul>
            </td>
        </tr>
        <tr style="background-color: #9900cc;">
            <td style="border: 1px solid black; padding: 8px; text-align: left;">11+ (Extreme)</td>
            <td style="border: 1px solid black; padding: 8px; text-align: left;">
                <ul>
                    <li>Tingkat bahaya ekstrem, diperlukan semua tindakan pencegahan karena kulit dan mata dapat rusak dalam hitungan menit.</li>
                    <li>Hindari paparan matahari langsung dan pastikan perlindungan maksimal.</li>
                    <li>Tetap di tempat teduh pada saat matahari terik siang hari.</li>
                    <li>Kenakan pakaian pelindung matahari, topi lebar, dan kacamata hitam yang menghalangi sinar UV, pada saat berada di luar ruangan.</li>
                    <li>Oleskan cairan pelembab tabir surya SPF 30+ setiap 2 jam bahkan pada hari berawan, setelah berenang atau berkeringat.</li>
                    <li>Permukaan yang cerah, seperti pasir, air, dan salju, akan meningkatkan paparan UV.</li>
                </ul>
            </td>
        </tr>
    </table>
    """,unsafe_allow_html=True,)


elif menu == "Data Historis":
    if data is not None and not data.empty:
        st.subheader("📊 Data Historis Indeks UV")
        selected_columns = ["Date", "Time", "Intensity", "Index"]
        data_filtered = data[selected_columns]

        col1, col2 = st.columns([2, 2.5]) 
        with col1:
            st.write("📋 **Tabel Data**")
            st.dataframe(data_filtered.tail(100).iloc[::-1].reset_index(drop=True), height=400)  
            
        with col2:
            st.write("📈 **Grafik Indeks UV**")
            latest_data = data.tail(100)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=latest_data["Waktu"], y=latest_data["Index"],
                                 mode='lines+markers', name='Indeks',
                                 line=dict(color='#6a0dad'), fill='tozeroy'))
            fig.update_layout(
                xaxis_title='Waktu',yaxis_title='Indeks UV',
                xaxis=dict(rangeslider=dict(visible=True)),
                height=500,margin=dict(t=30, b=20))
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Data tidak tersedia.")

# Custom Footer
st.markdown("""
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
