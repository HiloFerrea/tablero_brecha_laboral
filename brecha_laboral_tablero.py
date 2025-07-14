
import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Dashboard por Subcategoría", layout="wide")
st.title("Dashboard por Subcategoría - Brecha Laboral")

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

# Extraer textos de Titulo, Titulo_grafico y Fuente (primer valor válido)
titulo_tabla = df_filtrado["Titulo"].dropna().unique()
titulo_tabla = titulo_tabla[0] if len(titulo_tabla) > 0 else ""

titulo_grafico = df_filtrado["Titulo_grafico"].dropna().unique()
titulo_grafico = titulo_grafico[0] if len(titulo_grafico) > 0 else indicador

fuente = df_filtrado["Fuente"].dropna().unique()
fuente = fuente[0] if len(fuente) > 0 else ""

# Tabla con columna 'valor'
tabla = df_filtrado.pivot_table(
    index="Segmento",
    columns="Sexo",
    values="valor",
    aggfunc="first"
).reset_index()

st.subheader("📋 " + titulo_tabla)
st.dataframe(tabla, use_container_width=True)

# Gráfico con columna 'valor grafico'
st.subheader("📊 " + titulo_grafico)
fig = px.bar(
    df_filtrado,
    x="Segmento",
    y="valor grafico",
    color="Sexo",
    barmode="group",
    labels={"valor grafico": "Valor", "Segmento": "Categoría"},
)
fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig, use_container_width=True)

# Fuente
if fuente:
    st.caption("📌 Fuente: " + fuente)


