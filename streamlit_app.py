import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import plotly.graph_objects as go

# --- Konfigurasi Streamlit ---
st.set_page_config(page_title="Pemantauan Radiasi UV", layout="wide")

# --- Koneksi ke Google Sheets ---
url = "https://docs.google.com/spreadsheets/d/1SczaIV1JHUSca1hPilByJFFzOi5a8Hkhi0OemlmPQsY/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)
data = conn.read(spreadsheet=url, usecols=[0, 1, 2, 3], ttl=0)

# --- Preprocessing Data ---
data.dropna(inplace=True)  # Hapus data yang kosong jika ada

# Pastikan kolom waktu dalam format datetime
data['Waktu'] = pd.to_datetime(data['Waktu'])
data = data.sort_values(by='Waktu')

# --- Sidebar Navigasi ---
st.sidebar.title("Navigasi")
menu = st.sidebar.radio("Pilih Menu", ["Beranda", "Data UV", "Grafik"])

# --- Tampilan Beranda ---
if menu == "Beranda":
    st.markdown("<h1 style='text-align: center; color: purple;'>🌞 Sistem Pemantauan Radiasi UV</h1>", unsafe_allow_html=True)
    st.write("Pantau indeks UV secara real-time dan analisis historisnya dengan data terkini dari Google Sheets.")

# --- Tampilan Data UV ---
elif menu == "Data UV":
    st.subheader("📊 Data Historis Indeks UV")
    
    # Pewarnaan DataFrame
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

# --- Tampilan Grafik ---
elif menu == "Grafik":
    st.subheader("📈 Visualisasi Data Indeks UV")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['Waktu'], 
        y=data['Indeks UV'], 
        mode='lines+markers',
        line=dict(color='purple'),
        name='Indeks UV'
    ))
    
    fig.update_layout(
        title='Grafik Indeks UV Seiring Waktu',
        xaxis_title='Waktu',
        yaxis_title='Indeks UV',
        template='plotly_dark',
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)
    )
    
    st.plotly_chart(fig, use_container_width=True)
