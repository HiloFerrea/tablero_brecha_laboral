
import streamlit as st
import pandas as pd
import plotly.express as px

# Título del dashboard
st.title("Dashboard de indicadores laborales")

# Subir archivo Excel
archivo = st.file_uploader("Subí el archivo Excel", type=["xlsx"])

if archivo:
    df = pd.read_excel(archivo, sheet_name="DATOS")

    # Filtros
    indicador = st.selectbox("Seleccioná un indicador", sorted(df["pestaña"].dropna().unique()))

    df_filtrado = df[df["pestaña"] == indicador]

    segmentos = df_filtrado["Segmento"].dropna().unique()
    segmento = st.selectbox("Segmento", sorted(segmentos)) if len(segmentos) > 1 else segmentos[0]

    sexos = df_filtrado["Sexo"].dropna().unique()
    sexo = st.selectbox("Sexo", sorted(sexos)) if len(sexos) > 1 else sexos[0]

    df_final = df_filtrado[
        (df_filtrado["Segmento"] == segmento) &
        (df_filtrado["Sexo"] == sexo)
    ]

    # Verificación de datos disponibles
    if df_final.empty:
        st.warning("No hay datos para la combinación seleccionada.")
    else:
        # Gráfico
        df_final = df_final.sort_values("año")
        fig = px.line(df_final, x="año", y="valor grafico", title=indicador)
        st.plotly_chart(fig)

        # Mostrar tabla
        st.subheader("Datos utilizados")
        st.dataframe(df_final[["año", "Sexo", "Segmento", "valor grafico"]])
