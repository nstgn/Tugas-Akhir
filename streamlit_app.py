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

st.write("Data dari Google Sheets:", data)
