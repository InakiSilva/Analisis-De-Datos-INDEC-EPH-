import pandas as pd
import sys, os
import streamlit as st
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from constants import INDIVIDUAL_DATA_OUT_PATH
from utils_demografia import(
    distribucion_por_edad_y_sexo,
    edad_promedio_por_aglomerado,
    media_mediana_edad,
    evolucion_dependencia_demografica
)

if(st.session_state.get('updated')):
    # carga el csv de individuos generado 
    df = pd.read_csv(INDIVIDUAL_DATA_OUT_PATH, sep=";", encoding="utf-8")

    #---------------
    # Punto 1.3.1
    # distribución de la población por grupos de edad 

    distribucion_por_edad_y_sexo(df)

    st.markdown("---")
    #---------------
    # Punto 1.3.2
    #Promedio de edad por aglomerado 

    edad_promedio_por_aglomerado(df)

    st.markdown("---")

    #Punto 1.3.3
    #Evolucion de la dependencia demografica

    evolucion_dependencia_demografica(df)

    st.markdown("---")

    # Punto 1.3.4
    # Media y mediana de edad por período

    media_mediana_edad(df)

    st.markdown("---")
else:
    st.error("Primero debés actualizar el dataset para acceder a esta página. Dirigite a la sección \"Carga de datos\" para hacerlo.",icon="⚠️")

