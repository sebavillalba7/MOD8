import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN DE TEMA (DARK + PERSONALIZADO) ---
st.set_page_config(page_title="LESIONES DEPORTIVAS", page_icon="💪", layout="wide")

# --- CSS Personalizado para tabla y fondo ---
custom_css = """
<style>
body, .stApp {background-color: #102542 !important;}
thead tr th {
    background-color: #102542 !important;
    color: #fff !important;
    font-weight: bold !important;
    text-align: center !important;
}
tbody tr td {
    color: #fff !important;
    text-align: center !important;
}
.stDataFrame div[role="table"] {background: #102542 !important;}
.stDataFrame {color: #fff !important;}
/* Sidebar y selectbox */
.st-emotion-cache-1v0mbdj, .st-emotion-cache-6qob1r {background-color: #06101f !important;}
.st-emotion-cache-16idsys {color: #fff !important; font-weight: bold;}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- ENCABEZADO (LOGO + TITULO) ---
col1, col2 = st.columns([1, 7])
with col1:
    st.image("logo.png", width=90)  # Logo más pequeño (AJUSTA AQUÍ el tamaño)
with col2:
    st.markdown("<h1 style='text-align: right; letter-spacing:2px; font-size:2.5rem;'>DASHBOARD DE LESIONES DEPORTIVAS</h1>", unsafe_allow_html=True)  # Título a la derecha y en mayúsculas

# --- SUBTITULO ---
st.markdown("<h4 style='text-align:right;'>Mag. SEBASTIAN VILLALBA</h4>", unsafe_allow_html=True)  # Subtítulo debajo del título

# --- LECTURA DE DATOS ---
df = pd.read_excel("LESIONES_LONG.xlsx")

# --- PROCESAMIENTO DE FECHAS Y AÑOS ---
df['FECHA'] = pd.to_datetime(df['FECHA'], errors='coerce')
df['AÑO'] = df['FECHA'].dt.year
df['MES'] = df['FECHA'].dt.month

# --- SIDEBAR con MULTISELECT ---
with st.sidebar:
    st.markdown("<div style='text-align:center; font-size:2.2em;'>🟥</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; color:#fff; font-weight:bold;'>FILTRAR AÑO</h3>", unsafe_allow_html=True)
    anios = sorted(df['AÑO'].dropna().unique())
    anios_seleccionados = st.multiselect(
        "Selecciona uno o varios años",
        anios,
        default=anios[::-1]  # Todos seleccionados por defecto
    )

# --- FILTRO POR AÑO ---
df_filtro = df[df['AÑO'].isin(anios_seleccionados)]

# --- TITULO DE LA TABLA ---
st.markdown(
    "<h3 style='text-align:center; text-transform:uppercase;'><span style='font-size:1.4em;'>🗂️</span> Tabla de lesiones</h3>",
    unsafe_allow_html=True
)

# --- TABLA PERSONALIZADA ---
st.dataframe(df_filtro, use_container_width=True)


# --- GRAFICO DE BARRAS: Top 10 músculos ---
st.markdown(
    "<h3 style='text-align:center; text-decoration:underline;'>⚽️ TOP 10 LESIONES POR MÚSCULO</h3>",
    unsafe_allow_html=True
)
lesiones_musc = df_filtro['MUSC'].value_counts().head(10).sort_values(ascending=True)
fig_bar, ax_bar = plt.subplots(figsize=(8, 4))  # Más compacto
bars = ax_bar.barh(lesiones_musc.index, lesiones_musc.values, color='#2cff33')  # Verde fuerte
ax_bar.set_facecolor('#102542')
fig_bar.patch.set_facecolor('#102542')
ax_bar.spines[:].set_visible(False)
ax_bar.tick_params(axis='x', colors='#102542')
ax_bar.tick_params(axis='y', labelcolor='white', labelsize=12)
# Etiquetas de valor en blanco negrita
for i, v in enumerate(lesiones_musc.values):
    ax_bar.text(v + 0.2, i, str(v), color='white', fontweight='bold', va='center')
ax_bar.set_xlabel("")
ax_bar.set_ylabel("")
plt.tight_layout()
st.pyplot(fig_bar)

# --- GRAFICO LINEAL: Evolución mensual de lesiones ---
st.markdown(
    "<h3 style='text-align:center; text-decoration:underline;'>💊 EVOLUCIÓN MENSUAL DE LESIONES</h3>",
    unsafe_allow_html=True
)
df_filtro['MES_AÑO'] = df_filtro['FECHA'].dt.to_period('M')
lesiones_mes = df_filtro.groupby('MES_AÑO').size()
fig_linea, ax_linea = plt.subplots(figsize=(7, 2.5))  # Más chico
ax_linea.plot(
    lesiones_mes.index.astype(str),
    lesiones_mes.values,
    color='yellow',
    marker='o',
    markerfacecolor='blue',
    linewidth=2
)
ax_linea.set_facecolor('#102542')
fig_linea.patch.set_facecolor('#102542')
ax_linea.spines[:].set_visible(False)
ax_linea.tick_params(axis='x', labelcolor='white', labelsize=10, rotation=45)
ax_linea.tick_params(axis='y', left=False, labelleft=False)
# Etiquetas de valor en blanco negrita arriba de cada punto
for i, v in enumerate(lesiones_mes.values):
    ax_linea.text(i, v + 0.2, str(v), color='white', fontweight='bold', ha='center', va='bottom')
ax_linea.set_xlabel("")
ax_linea.set_ylabel("")
plt.tight_layout()
st.pyplot(fig_linea)

# --- GRAFICO LINEAL: Días de baja ---
if 'DAY_OFF_DXT' in df_filtro.columns:
    st.markdown(
        "<h3 style='text-align:center; text-decoration:underline;'>👨‍⚕️ DÍAS DE BAJA POR LESIONES</h3>",
        unsafe_allow_html=True
    )
    days_off = df_filtro.groupby('MES_AÑO')['DAY_OFF_DXT'].sum()
    fig2, ax2 = plt.subplots(figsize=(7, 2.5))  # Más chico
    ax2.plot(
        days_off.index.astype(str),
        days_off.values,
        color='red',
        marker='s',
        markerfacecolor='blue',
        linewidth=2
    )
    ax2.set_facecolor('#102542')
    fig2.patch.set_facecolor('#102542')
    ax2.spines[:].set_visible(False)
    ax2.tick_params(axis='x', labelcolor='white', labelsize=10, rotation=45)
    ax2.tick_params(axis='y', left=False, labelleft=False)
    for i, v in enumerate(days_off.values):
        ax2.text(i, v + 0.2, str(int(v)), color='white', fontweight='bold', ha='center', va='bottom')
    ax2.set_xlabel("")
    ax2.set_ylabel("")
    plt.tight_layout()
    st.pyplot(fig2)

