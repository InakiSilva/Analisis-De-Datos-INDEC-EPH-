import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from constants import DATA_OUT_PATH
from utils_edu import nivel_ed_anios
from utils_edu import boton_descarga
from utils_edu import alfabetizacion_todos_los_anios

archivo = DATA_OUT_PATH / "usus_individual.csv"


#debug
print("Python ejecutándose desde:", sys.executable)

#abro el csv con pandas
df = pd.read_csv(archivo, delimiter=';', low_memory=False)
# recorto solo las columnas que necesito
df = df[['ANO4','PONDERA','NIVEL_ED_str','CH06','CH09']]

st.title('Educación')

# punto 1

# Selección de año
anos_disponibles = sorted(df['ANO4'].unique())
anio = st.selectbox("Seleccione año a consultar: ",anos_disponibles)

nivel_ed_anios(df,anio)

# punto 3 - Mostrar y permitir descargar el ranking
ranking = DATA_OUT_PATH / "ranking_aglomerados.csv"
descarga = pd.read_csv(ranking, delimiter=',')
boton_descarga(descarga)


# punto 4 
#punto 4
st.subheader("Alfabetización por años")
alfabetizacion_todos_los_anios(df)