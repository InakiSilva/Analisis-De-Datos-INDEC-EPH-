import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from constants import INDIVIDUAL_DATA_OUT_PATH , FILE_RANKING_CINCO_AGLOMERADOS 
from utils_edu import nivel_ed_anios
from utils_edu import boton_descarga
from utils_edu import alfabetizacion_todos_los_anios
from utils_edu import nivel_educativo_por_grupo_etario

if(st.session_state.get('updated')):
    archivo = INDIVIDUAL_DATA_OUT_PATH 

    #abro el csv con pandas
    df = pd.read_csv(archivo, delimiter=';', low_memory=False)
    # recorto solo las columnas que necesito
    df = df[['ANO4','PONDERA','NIVEL_ED_str','CH06','CH09']]

    st.title('📚Educación')

    # punto 1

    # Selección de año
    anos_disponibles = sorted(df['ANO4'].unique())
    anio = st.selectbox("Seleccione año a consultar: ",anos_disponibles)

    nivel_ed_anios(df,anio)

    #punto 2
    nivel_educativo_por_grupo_etario(df)

    # punto 3 - Mostrar y permitir descargar el ranking
    descarga = pd.read_csv(FILE_RANKING_CINCO_AGLOMERADOS, delimiter=',')
    boton_descarga(descarga)


    # punto 4 
    #punto 4
    st.header("📖Alfabetización por años(mayores de 6 años)")
    alfabetizacion_todos_los_anios(df)
else:
    st.error("Primero debés actualizar el dataset para acceder a esta página. Dirigite a la sección \"Carga de datos\" para hacerlo.",icon="⚠️")