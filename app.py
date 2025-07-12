import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN DE TEMA (DARK) ---
st.set_page_config(page_title="Lesiones Deportivas", page_icon="💪", layout="wide")

custom_css = """
<style>
body {
    background-color: #102542;
    color: #ffffff;
}
h1, h2, h3, h4, h5, h6, .stTextInput>div>div>input {
    color: #ffffff !important;
}
.stApp {
    background-color: #102542;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- LOGO ---
st.image("logo.png", width=180)  # Cambia por la URL o ruta de tu logo

st.title("Dashboard de Lesiones Deportivas")
st.markdown("Filtrado y análisis de lesiones musculares")

# --- LECTURA DE DATOS ---
df = pd.read_excel("LESIONES_LONG.xlsx")

# --- PROCESAMIENTO DE FECHAS Y AÑOS ---
df['FECHA'] = pd.to_datetime(df['FECHA'], errors='coerce')
df['AÑO'] = df['FECHA'].dt.year
df['MES'] = df['FECHA'].dt.month

# --- FILTRO POR AÑO ---
anios = sorted(df['AÑO'].dropna().unique())
anio = st.sidebar.selectbox("Selecciona un año", anios, index=len(anios)-1)  # Último año por defecto

df_filtro = df[df['AÑO'] == anio]

st.subheader(f"Tabla de lesiones en {anio}")
st.dataframe(df_filtro.head(100))  # Cambia el 100 si quieres mostrar más/menos filas

# --- GRAFICO DE BARRAS: Lesiones por músculo ---
st.subheader("Cantidad de lesiones por músculo")
lesiones_musc = df_filtro['MUSC'].value_counts()
st.bar_chart(lesiones_musc)

# --- GRAFICO LINEAL: Lesiones por mes ---
st.subheader("Lesiones por mes y año")
df_filtro['MES_AÑO'] = df_filtro['FECHA'].dt.to_period('M')
lesiones_mes = df_filtro.groupby('MES_AÑO').size()

fig, ax = plt.subplots()
lesiones_mes.plot(ax=ax, marker='o')
ax.set_xlabel("Mes y año")
ax.set_ylabel("Cantidad de lesiones")
ax.set_title("Evolución mensual de lesiones")
st.pyplot(fig)

# --- GRAFICO LINEAL: Días de baja por mes ---
if 'DAY_OFF_DXT' in df_filtro.columns:
    st.subheader("Días de baja (DAY_OFF_DXT) por mes")
    days_off = df_filtro.groupby('MES_AÑO')['DAY_OFF_DXT'].sum()
    fig2, ax2 = plt.subplots()
    days_off.plot(ax=ax2, marker='s', color='#33BFFF')
    ax2.set_xlabel("Mes y año")
    ax2.set_ylabel("Días de baja")
    ax2.set_title("Días de baja por lesiones (mensual)")
    st.pyplot(fig2)
