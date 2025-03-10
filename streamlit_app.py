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

# Sidebar Menu
menu = st.sidebar.selectbox("Menu", ["Beranda", "Data UV", "Grafik"])

if menu == "Beranda":
    st.title("Sistem Pemantauan Radiasi UV")
    st.write("Selamat datang di sistem pemantauan radiasi UV berbasis IoT dan AI.")
    st.image("https://source.unsplash.com/800x400/?sunlight")

elif menu == "Data UV":
    st.title("Data Historis Indeks UV")
    st.dataframe(data[["Waktu", "Intensity", "Index"]])

elif menu == "Grafik":
    st.title("Visualisasi Data Indeks UV")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data["Waktu"], y=data["Index"], mode='lines', name='Indeks UV', line=dict(color='orange')))
    
    fig.update_layout(title="Grafik Indeks UV dari Data Historis",
                      xaxis_title="Waktu",
                      yaxis_title="Indeks UV",
                      template="plotly_dark")
    
    st.plotly_chart(fig)
