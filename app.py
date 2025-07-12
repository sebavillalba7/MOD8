
import streamlit as st
import pandas as pd

st.title("Mi App Streamlit en PythonAnywhere")
st.write("Esta es una demo usando datos locales")

# Lee tu base de datos 
df = pd.read_excel('db_completo_2.xlsx')
st.write("Primeras filas de la base de datos:")
st.dataframe(df.head())
