import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Simulasi data
latest_data = {'Index': 5, 'Time': '12:30'}  # Gantilah dengan data aktual
future_df = pd.DataFrame({
    'Time': pd.date_range(start='13:00', periods=5, freq='H'),
    'Predicted Index': [2, 4, 7, 9, 11]
})

# Sidebar Menu
st.sidebar.title("Navigasi")
menu = st.sidebar.radio("Pilih Halaman:", ["Dashboard", "Prediksi", "Tabel Proteksi"])

# Header Kustom
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

st.markdown("<h1 style='text-align: center;'>UV Index Monitoring</h1>", unsafe_allow_html=True)

if menu == "Dashboard":
    uv_index = latest_data['Index']

    # Gauge Chart
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
                {'range': [10, 11], 'color': "#9900cc"},
            ]
        }
    ))
    fig.update_layout(margin=dict(t=30, b=30, l=30, r=30))
    st.plotly_chart(fig, use_container_width=True)
    
    # Informasi Tambahan
    st.markdown(f"""
    <div style="text-align: center;">
        <p><b>Pukul:</b> {latest_data['Time']}</p>
    </div>
    """, unsafe_allow_html=True)

elif menu == "Prediksi":
    st.markdown("<h1 style='text-align: center;'>UV Index Prediction</h1>", unsafe_allow_html=True)
    cols = st.columns(len(future_df))
    for i, row in future_df.iterrows():
        with cols[i]:
            uv_level = row["Predicted Index"]
            color_map = [(3, "🟢", "Low", "#00ff00"),
                         (6, "🟡", "Moderate", "#ffe600"),
                         (8, "🟠", "High", "#ff8c00"),
                         (11, "🔴", "Very High", "#ff0000"),
                         (float("inf"), "🟣", "Extreme", "#9900cc")]
            for limit, icon, desc, bg_color in color_map:
                if uv_level < limit:
                    break
            
            st.markdown(f"""
            <div style="text-align:center; padding:10px; border-radius:5px; background-color:{bg_color};">
                <h3 style="color:white;">{row['Time'].strftime('%H:%M')}</h3>
                <h2 style="color:white;">{icon} {uv_level}</h2>
                <p style="color:white;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

elif menu == "Tabel Proteksi":
    st.markdown("<h1 style='text-align: center;'>Tabel Saran Proteksi</h1>", unsafe_allow_html=True)
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
                    <li>Kenakan kacamata hitam pada hari cerah.</li>
                    <li>Gunakan pelembab tabir surya SPF 30+.</li>
                </ul>
            </td>
        </tr>
        <tr style="background-color: #ffff00;">
            <td style="border: 1px solid black; padding: 8px; text-align: left;">3-5 (Moderate)</td>
            <td style="border: 1px solid black; padding: 8px; text-align: left;">
                <ul>
                    <li>Gunakan pakaian pelindung dan topi.</li>
                    <li>Oleskan tabir surya SPF 30+ setiap 2 jam.</li>
                </ul>
            </td>
        </tr>
        <tr style="background-color: #ff6600;">
            <td style="border: 1px solid black; padding: 8px; text-align: left;">6-7 (High)</td>
            <td style="border: 1px solid black; padding: 8px; text-align: left;">
                <ul>
                    <li>Kurangi paparan matahari antara pukul 10-16.</li>
                    <li>Gunakan perlindungan tambahan seperti payung atau shade.</li>
                </ul>
            </td>
        </tr>
    </table>
    """, unsafe_allow_html=True)
