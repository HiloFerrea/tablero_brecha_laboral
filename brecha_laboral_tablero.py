
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard de Brecha Laboral", layout="wide")

st.title("Dimensión - Brecha Laboral")

# Cargar archivo local ya incluido en el repo
df = pd.read_excel("brecha_laboral_tablero.xlsx", sheet_name="DATOS")

# Filtros principales
dimension = st.sidebar.selectbox("Seleccioná una dimensión", sorted(df["DIMENSION"].dropna().unique()))

df_dim = df[df["DIMENSION"] == dimension]
indicadores = df_dim["pestaña"].dropna().unique()
indicador = st.sidebar.selectbox("Seleccioná un indicador", sorted(indicadores))

df_ind = df_dim[df_dim["pestaña"] == indicador]
anios = df_ind["año"].dropna().unique()
anio = st.sidebar.selectbox("Seleccioná un año", sorted(anios))

# Filtrado final
df_filtrado = df_ind[df_ind["año"] == anio]

# Tabla: filas = segmento, columnas = sexo
tabla = df_filtrado.pivot_table(
    index="Segmento",
    columns="Sexo",
    values="valor grafico",
    aggfunc="first"
).reset_index()

st.subheader("📋 Tabla comparativa por sexo")
st.dataframe(tabla, use_container_width=True)

# Gráfico de barras agrupadas
st.subheader("📊 Comparación gráfica")
fig = px.bar(
    df_filtrado,
    x="Segmento",
    y="valor grafico",
    color="Sexo",
    barmode="group",
    labels={"valor grafico": "Valor", "Segmento": "Categoría"},
    title=f"{indicador} - Año {anio}"
)
fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig, use_container_width=True)

