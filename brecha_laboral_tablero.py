
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Dimensión económica", layout="wide")
st.title("Inserción laboral y brecha salarial")

archivo = "brecha_laboral_tablero.xlsx"
if not os.path.exists(archivo):
    st.error(f"⚠️ El archivo '{archivo}' no se encuentra en el repositorio.")
    st.stop()

df = pd.read_excel(archivo, sheet_name="DATOS")

# Filtros principales
subcategoria = st.sidebar.selectbox("Seleccioná una subcategoría", sorted(df["SUBCATEGORIA"].dropna().unique()))
df_sub = df[df["SUBCATEGORIA"] == subcategoria]

indicadores = df_sub["pestaña"].dropna().unique()
indicador = st.sidebar.selectbox("Seleccioná un indicador", sorted(indicadores))
df_ind = df_sub[df_sub["pestaña"] == indicador]

anios = df_ind["año"].dropna().unique()
anio = st.sidebar.selectbox("Seleccioná un año", sorted(anios))
df_filtrado = df_ind[df_ind["año"] == anio]

# Extraer textos
titulo_tabla = df_filtrado["Titulo"].dropna().unique()
titulo_tabla = titulo_tabla[0] if len(titulo_tabla) > 0 else ""

titulo_grafico = df_filtrado["Titulo_grafico"].dropna().unique()
titulo_grafico = titulo_grafico[0] if len(titulo_grafico) > 0 else indicador

fuente = df_filtrado["Fuente"].dropna().unique()
fuente = fuente[0] if len(fuente) > 0 else ""

periodo = df_filtrado["GREO_PERIODO"].dropna().unique()
periodo = periodo[0] if len(periodo) > 0 else ""

# Añadir año y periodo a los títulos
sufijo = f" — {periodo} (Año {anio})"
titulo_tabla += sufijo
titulo_grafico += sufijo

# Tabla con columna 'valor', usando 'indicador' como índice
tabla = df_filtrado.pivot_table(
    index="indicador",
    columns="Sexo",
    values="valor",
    aggfunc="first"
).reset_index()

st.markdown(f"<p style='font-size:16px; font-weight:bold'>{titulo_tabla}</p>", unsafe_allow_html=True)
st.dataframe(tabla, use_container_width=True)

# Colores personalizados
colores_personalizados = {
    "Mujer": "#006400",  # Verde oscuro
    "Varón": "#90EE90"   # Verde claro
}

# Gráfico de barras con plotly.graph_objects
st.markdown(f"<p style='font-size:16px; font-weight:bold'>{titulo_grafico}</p>", unsafe_allow_html=True)

fig = go.Figure()

for sexo in df_filtrado["Sexo"].unique():
    df_sexo = df_filtrado[df_filtrado["Sexo"] == sexo]
    fig.add_trace(go.Bar(
        x=df_sexo["indicador"],
        y=df_sexo["valor grafico"],
        name=sexo,
        marker_color=colores_personalizados.get(sexo, "#CCCCCC")
    ))

fig.update_layout(
    barmode="group",
    xaxis_title="Indicador",
    yaxis_title="Valor",
    xaxis_tickangle=-45,
    legend_title="Sexo"
)

st.plotly_chart(fig, use_container_width=True)

# Fuente
if fuente:
    st.caption("**Fuente:** " + fuente)

