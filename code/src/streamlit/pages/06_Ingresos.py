import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from constants import CANASTA_FILE_PATH, FILES_HOGARES_DIRECTORY
from obtener_fechas import streamlit_get_quarters

def read_csv(path, delimiter=',', usecols=None):
    """
    Lee un archivo CSV con Pandas y retorna su data frame o produce un mensaje de error
    en Streamlit y corta la ejecución si el archivo no existe o no se tienen permisos para leerlo
    Params:
        path (Path): Path del archivo a leer.
        delimiter (str, optional): Delimitador del archivo CSV.
        usecols (list, optional): Lista de columnas a leer del archivo, por defecto es None.
    Returns:
        DataFrame: Archivo CSV leído como un DataFrame.
    """
    try:
        return pd.read_csv(path, delimiter=delimiter, usecols=usecols)
    except FileNotFoundError:
        st.error(f"El archivo {path} no existe.")
    except PermissionError:
        st.error(f"No hay permisos para leer el archivo {path}.")
    st.stop()

if(st.session_state.get('updated')):
    st.title("🪙Ingresos")
    st.write(f"""
    ## 🧾 Información

    En esta página se puede contabilizar la cantidad de familias **por debajo de la línea de pobreza o indigencia promedio del trimestre**, para un año y trimestre específicos.

    Los **años y trimestres disponibles** para seleccionar corresponden a aquellos presentes tanto en los archivos de la carpeta **hogares** (`{FILES_HOGARES_DIRECTORY}`) como en el archivo de la **canasta básica** (`{CANASTA_FILE_PATH}`).

    > ℹ️ **Importante:** Los resultados obtenidos **no tienen valor estadístico**, ya que solo se incluyen los hogares que:
    > - 👨‍👩‍👧‍👦 Tienen exactamente **4 integrantes**.
    > - 📝 Han declarado el **ingreso total familiar** en la EPH del trimestre seleccionado.
    """)


    # Leo el archivo de canasta basica y convierto la columna 'indice_tiempo' a timestamp
    canasta_df = read_csv(CANASTA_FILE_PATH, usecols=['indice_tiempo','linea_indigencia','linea_pobreza']).dropna()
    try:
        canasta_df.indice_tiempo = pd.to_datetime(canasta_df.indice_tiempo,format="%Y-%m-%d")
    except ValueError:
        st.error("La fecha en algun mes de la canasta básica no cumple el formato '%Y-%m-%d' o no es un numero.")
        st.stop()

    # Obtengo todos los trimestres existentes en archivos de hogares
    quarters = streamlit_get_quarters(file_type='hogar')

    # Todos los años que existen en la canasta
    years_in_canasta = canasta_df.indice_tiempo.dt.year.unique()

    # Años que hay en los archivos y en la canasta
    years_options = sorted({year for year, _ in quarters if year in years_in_canasta})

    year = st.selectbox("Seleccione el año", years_options, index=None, placeholder="Año")
    if year:
        # Obtengo los trimestres que estan en los archivos y los que estan en la canasta para ese año
        file_quarters = {q for y, q in quarters if y == year}
        df_quarters =  set(canasta_df.indice_tiempo[(canasta_df.indice_tiempo.dt.year == year)].dt.quarter)
        
        # Las opciones de trimestres son los trimestres que estan en los archivos de hogares y de canasta ordenados
        quarter_options = sorted(file_quarters & df_quarters)

        # Se establecen los trimestres disponibles como opciones
        quarter = st.selectbox("Seleccione el trimestre", quarter_options, index=None, placeholder="Trimestre")


    if st.button("Contabilizar familias"):
        if year and quarter:
            # Ruta al archivo seleccionado
            file_name = f"usu_hogar_T{quarter}{year - 2000:02d}.txt"
            file_path = FILES_HOGARES_DIRECTORY / file_name

            # Obtener promedio de linea de pobreza e indigencia
            selected_canasta_df = canasta_df[(canasta_df.indice_tiempo.dt.year == year) & (canasta_df.indice_tiempo.dt.quarter == quarter)]
            try:
                indigence_average = selected_canasta_df.linea_indigencia.astype(float).mean()
                poverty_average = selected_canasta_df.linea_pobreza.astype(float).mean()
            except ValueError:
                st.error("Error: Hay valores no numéricos en las columnas 'linea_indigencia' o 'linea_pobreza' del archivo de canasta básica.")
                st.stop()

            # Leo el archivo y me quedo con las columnas requeridas de los hogares con 4 integrantes que hayan respondido su ITF
            file_df = read_csv(file_path, delimiter=';', usecols=["PONDERA","IX_TOT","ITF","DECIFR"]).dropna()
            try:
                file_df = file_df[(file_df["IX_TOT"].astype(int) == 4) & (~file_df["DECIFR"].astype(str).isin(['12', '13']))][["PONDERA", "ITF"]].copy()
            except ValueError:
                st.error(f"Error: Hay valores no numéricos en la columna 'IX_TOT' del archivo {file_name}.")
                st.stop()

            # Convertir columnas necesarias de hogares solo una vez
            try:
                file_df["ITF"] = file_df["ITF"].astype(float)
                file_df["PONDERA"] = file_df["PONDERA"].astype(int)
            except ValueError:
                st.error(f"Error: Hay valores no numéricos en las columnas 'ITF' o 'PONDERA' del archivo {file_name}.")
                st.stop()

            # Contabilizar hogares bajo la linea de pobreza, bajo la linea de indigencia y totales
            houses_amount = file_df["PONDERA"].sum()
            indigence_amount = file_df[indigence_average > file_df["ITF"]]["PONDERA"].sum()
            poverty_amount = file_df[(poverty_average > file_df["ITF"]) & (file_df["ITF"] >= indigence_average)]["PONDERA"].sum()

            # Porcentajes
            if houses_amount > 0:
                indigence_percentage = indigence_amount / houses_amount * 100
                poverty_percentage = poverty_amount / houses_amount * 100
            else:
                indigence_percentage = 0
                poverty_percentage = 0
            
            # Mostrar resultados
            col1, col2 = st.columns(2,border=True)
            col1.metric(f"Línea de pobreza promedio", f"${poverty_average:.2f}")
            col2.metric(f"Línea de indigencia promedio", f"${indigence_average:.2f}")
            col1.metric("Familias bajo la línea de pobreza promedio",f"{poverty_amount} ({poverty_percentage:.2f}%)")
            col2.metric("Familias bajo la línea de indigencia promedio",f"{indigence_amount} ({indigence_percentage:.2f}%)")
        else:
            st.error("Por favor, seleccione un año y un trimestre.")

else:
    st.error("Primero debés actualizar el dataset para acceder a esta página. Dirigite a la sección \"Carga de datos\" para hacerlo.",icon="⚠️")
