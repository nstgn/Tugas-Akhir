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
menu = st.sidebar.radio("Pilih Menu", ["Beranda", "Indeks UV", "Tabel Proteksi", "Data Historis"])

# Tampilan Beranda
if menu == "Beranda":
    st.markdown(""" 
    <h1 style='text-align: center; color: #6a0dad;'>🌞 SISTEM PREDIKSI INDEKS UV</h1>
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
        margin=dict(t=30, b=30, l=30, r=30),
        height=250, width=400)
    
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


elif menu == "Tabel Proteksi":
    st.markdown("""
    <h1 style="text-align: center;margin-top: 40px; margin-bottom: 10px;">Tabel Saran Proteksi</h1>
    """,unsafe_allow_html=True,)
    
    st.markdown(
    """
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
    """,
    unsafe_allow_html=True,
)


elif menu == "Data Historis":
    if data is not None and not data.empty:
        st.subheader("📊 Data Historis Indeks UV")

        # Memilih hanya kolom yang diperlukan
        selected_columns = ["Date", "Time", "Index", "Intensity"]
        data_filtered = data[selected_columns]  # Hanya menyimpan kolom yang diperlukan

        # Membuat dua kolom: kiri (tabel) & kanan (grafik)
        col1, col2 = st.columns([1, 2])  # Kolom kiri lebih kecil dari kanan

        with col1:
            st.write("📋 **Tabel Data (Terbaru di Atas)**")
            st.dataframe(data_filtered.tail(20).iloc[::-1], height=400)  # Urutan terbaru di atas

        with col2:
            st.write("📈 **Grafik Indeks UV**")
            fig = px.line(
                data, 
                x="Date",  # Gunakan Date sebagai sumbu X untuk visualisasi waktu
                y="Index", 
                markers=True, 
                title="Grafik Indeks UV Seiring Waktu",
                labels={"Index": "Indeks UV", "Date": "Tanggal"}
            )
            fig.update_traces(line=dict(color="purple"), fill="tozeroy")  # Warna & area fill
            fig.update_layout(xaxis=dict(rangeslider=dict(visible=True)))  # Scroll horizontal

            st.plotly_chart(fig, use_container_width=True)  # Grafik responsif
    else:
        st.warning("⚠️ Data tidak tersedia.")
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
