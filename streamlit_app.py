import streamlit as st
from streamlit_gsheets import GSheetsConnection

url = "https://docs.google.com/spreadsheets/d/1W9WYq245Q7g4VYn0BWt7x5DcMnhba3-rugeMu2TPM60/edit?gid=0#gid=0"

conn = st.connection("gsheets", type=GSheetsConnection)

data = conn.read(spreadsheet=url, usecols=[0, 1,2,3])
st.dataframe(data)