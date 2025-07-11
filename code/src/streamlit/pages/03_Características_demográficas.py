import pandas as pd
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from constants import INDIVIDUAL_DATA_OUT_PATH
from utils_demografia import distribucion_por_edad_y_sexo
from prom_ed_aglom import edad_promedio_por_aglomerado

# carga el csv de individuos generado 
df = pd.read_csv(INDIVIDUAL_DATA_OUT_PATH, sep=";", encoding="utf-8")

#---------------
# Punto 1.3.1
# distribución de la población por grupos de edad 

distribucion_por_edad_y_sexo(df)

#---------------
# Punto 1.3.2
#Promedio de edad por aglomerado 

df = pd.read_csv (INDIVIDUAL_DATA_OUT_PATH, sep=";", encoding="utf-8")
edad_promedio_por_aglomerado(df)