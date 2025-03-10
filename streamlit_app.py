#1 Import Library
import numpy as np
import pandas as pd
import tensorflow as tf
import streamlit as st
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from streamlit_gsheets import GSheetsConnection

#2 Input Data
url = "https://docs.google.com/spreadsheets/d/1W9WYq245Q7g4VYn0BWt7x5DcMnhba3-rugeMu2TPM60/edit?gid=0#gid=0"
conn = st.connection("gsheets", type=GSheetsConnection)
data =  conn.read(spreadsheet=url, usecols=[0, 1, 2, 3])

#3 Pre-Processing Data
data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
data.set_index('Datetime', inplace=True)
data = data[['Index']].copy()
date_range = pd.date_range(start=data.index.min(), end=data.index.max(), freq='2T')
date_range = date_range[(date_range.hour >= 6) & (date_range.hour <= 18)]
data = data.reindex(date_range)
data['Index'].interpolate(method='linear', inplace=True)



# Custom Header
st.markdown(
    """
    <style>
    .header { background-color: #D6D6F5; padding: 10px; text-align: center; border-radius: 7px;}
    .header img { width: 60px;  }
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

# Membuat gauge chart
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

st.write("Data dari Google Sheets:", data)
