import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Dummy data (gantilah dengan data asli dari Google Sheets)
data = pd.DataFrame({
    "Waktu": pd.date_range(start="2025-03-01 06:00", periods=10, freq="H"),
    "Indeks UV": [2, 3, 5, 6, 8, 10, 9, 7, 5, 3]
})

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
