
import sys
from pathlib import Path

# Agrega el path del proyecto (uno o dos niveles arriba de src)
sys.path.append(str(Path(__file__).resolve().parents[2]))

import streamlit as st

st.header('Encuest.AR')

st.write("""Encuest.AR es una aplicación web diseñada para **transformar datos crudos en información comprensible**. Su funcionamiento principal consiste en:

1. **Carga y jerarquización** de datasets trimestrales de la encuesta permanente de hogares(EPH) 🗂️.
2. **Análisis estadístico automatizado** para el calculo de métricas.

---

**¿Qué información almacena la EPH?** 📊

- **Identificadores geográficos**: provincia, región, aglomerado.  
- **Características del hogar**: número de integrantes, régimen de tenencia de la vivienda 🏠.  
- **Datos individuales**: edad, sexo, nivel de instrucción, condición de actividad (ocupado, desocupado, inactivo).  
- **Variables socioeconómicas**: ingreso individual y del hogar, fuente principal de ingresos, asistencia social.  

> ℹ️ *Con esta estructura, Encuest.AR permite analizar y comparar tendencias socioeconómicas de la población argentina de manera ágil y amigable.*

""")