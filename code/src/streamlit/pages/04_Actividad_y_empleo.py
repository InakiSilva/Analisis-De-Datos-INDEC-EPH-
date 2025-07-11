import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from constants import DATA_OUT_PATH
from utils_actividad_y_empleo import *

if(st.session_state.get('updated')):
    archivoIndividuos = DATA_OUT_PATH / "usus_individual.csv"

    df = pd.read_csv(archivoIndividuos, delimiter=';')

    # Título principal
    st.title("📊 Actividad y Empleo")

    # lectura de un año
    anos_disponibles = sorted(df["ANO4"].unique())
    anio = st.selectbox("Seleccione año a consultar: ", anos_disponibles)

    # En base al año ingresado, leo un trimestre
    trimestres_disponibles = sorted(
        df.loc[df["ANO4"] == anio, "TRIMESTRE"].unique())
    trimestre = st.selectbox(
        "Seleccione un trimestre a consultar : ", trimestres_disponibles)

    desocupacion_por_nivel_ed(df, int(anio), int(trimestre))

    evolucion_desempleo_empleo(df)

    informacion_ocupacion_por_aglomerado (df)

    aglomerado_mapa_empleo_desempleo (df)
else:
    st.error("Primero debés actualizar el dataset para acceder a esta página. Dirigite a la sección \"Carga de datos\" para hacerlo.",icon="⚠️")