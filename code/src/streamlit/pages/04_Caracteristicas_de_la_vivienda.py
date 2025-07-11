import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from constants import HOGAR_DATA_OUT_PATH
from utils_caracteristicas_vivienda import tipo_viviendas, tipo_piso_viviendas, porcentaje_banio_aglomerados

st.title("Características de la vivienda")

df = pd.read_csv(HOGAR_DATA_OUT_PATH, delimiter=";")

anos_disponibles = sorted(df["ANO4"].unique())
opcion = st.selectbox("Elegir un año", options= ["TODOS"] + list(anos_disponibles))

if opcion == "TODOS":
    st.text("Se mostrarán todos los datos.")
    df_filtrado = df.copy()

if opcion != "TODOS":
    opcion = int(opcion)
    df_filtrado = df[df["ANO4"] == opcion]

cantidad_viviendas = df_filtrado["PONDERA"].sum()

st.metric("Cantidad de viviendas", cantidad_viviendas)

if cantidad_viviendas == 0:
    st.text("No hay datos de este año! Elegí otro.")
else:
    tipo_viviendas(df_filtrado)
    tipo_piso_viviendas(df_filtrado)
    porcentaje_banio_aglomerados(df_filtrado)