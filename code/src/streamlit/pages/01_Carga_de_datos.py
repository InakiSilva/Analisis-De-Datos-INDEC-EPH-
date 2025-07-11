
import streamlit as st
import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from recorrer_y_unir_files import unir_files
from obtener_fechas import streamlit_get_quarters,streamlit_get_quarters_range
from utils_hogares import create_columns_hogares
from utils_individuos import create_columns_individuos
from ranking_cinco import *

def show_quarters_range():
    """
    Obtiene el año y trimestre mas antiguo y mas actual de los archivos disponibles y lo muestra
    como un mensaje de exito en Streamlit si hay archivos disponibles o muestra un mensaje de error si no los hay 

    return:
        retorna un valor booleano si existen datos o si las carpetas de archivos hogares e individuos estan vacias

    """
    quarters_range = streamlit_get_quarters_range()
    
    if quarters_range:
        first_quarter = quarters_range[0]
        last_quarter = quarters_range[1]
        st.success(f"Existen archivos desde {first_quarter[1]}/{first_quarter[0]} hasta {last_quarter[1]}/{last_quarter[0]}")
        return True
    else:
        st.error("No hay archivos disponibles")
        return False

def check_files():
    """
    Verifica los archivos de las carpetas 'hogares' e 'individuos' para corroborar que cada archivo de individuos 
    tiene su archivo correspondiente de hogares en el mismo trimestre y viceversa. Luego, muestra un mensaje de éxito 
    en Streamlit si el chequeo resulta exitoso o uno o más mensajes de error indicando los archivos faltantes.
    Returns:
        Boolean: True si el checkeo resultó exitoso sino False.
    """

    def get_difference_error(diff,file_type):
        """
        Devuelve un mensaje de error formateado para el archivo faltante.
        Params:
            diff (tuple): Tupla con año y trimestre del archivo faltante en el formato (2023, 2).
            file_type (str): Tipo de archivo faltante, debe ser "hogares" o "individuos".
        Returns:
            str: Mensaje de error para el archivo faltante.
        """
        year = diff[0]
        quarter = diff[1]
        name_date = f"{quarter}{year-2000}"
        if file_type == "hogares":
            return f"Falta el archivo de hogares para el trimestre {quarter}/{year} llamado usu_hogar_T{name_date}.txt correspondiente a usu_individual_T{name_date}.txt"
        return f"Falta el archivo de individuos para el trimestre {quarter}/{year} llamado usu_individual_T{name_date}.txt correspondiente a usu_hogar_T{name_date}.txt"

    hogares_files = streamlit_get_quarters(file_type='hogar')
    individuos_files = streamlit_get_quarters(file_type='individual')

    if hogares_files == individuos_files:
        st.success("El chequeo resultó exitoso y no se encontraron inconsistencias.")
        return True
    else:
        differences_hogares = individuos_files - hogares_files
        differences_individuos = hogares_files - individuos_files

        for diff in differences_hogares:
            st.error(get_difference_error(diff, "hogares"))

        for diff in differences_individuos:
            st.error(get_difference_error(diff,"individuos"))
        return False

st.title("Carga de datos")

if show_quarters_range() :  
    # Botón para actualizar
    if st.button("Actualizar dataset"):
        st.session_state.updated = False
        if not check_files():
            st.error("No se puede actualizar el dataset con archivos faltantes")
        else:
            with st.spinner("Actualizando dataset..."):
                # 1. Unir archivos
                try:
                    merge_success = unir_files()
                except FileNotFoundError:
                    st.error("No existe la carpeta de hogares o la de individuos.")
                    st.stop()
                except NotADirectoryError:
                    st.error(f"La carpeta de hogares, individuos o data_out no es un directorio")
                    st.stop()
                except PermissionError:
                    st.error("No se tienen permisos en la carpeta de hogares, individuos o data_out.")
                    st.stop()
                except Exception as e:
                    st.error(f"Error al actualizar el dataset: {e}.")
                    st.stop()

                if merge_success:   
                    # 2. Crear columnas 
                    try:
                        create_columns_individuos()
                        create_columns_hogares()
                        guardar_ranking_aglomerados (calcular_datos_hogares_por_aglomerado ())
                    except FileNotFoundError:
                        st.error("No existe el archivo de individuos u hogares.")
                        st.stop()
                    except PermissionError:
                        st.error("No se tienen permisos para leer/escribir el archivo de individuos u hogares.")
                        st.stop()
                    except KeyError:
                        st.error("Faltan columnas vitales en el archivo de individuos u hogares.")
                        st.stop()
                    except Exception as e:
                        st.error(f"Error al generar las columnas nuevas en el dataset: {e}.")
                        st.stop()
                    st.session_state.updated = True
                    st.success("Dataset actualizado")
                else:
                    st.error("No se puede actualizar el dataset sin archivos")
    # Botón para comprobar archivos faltantes
    if st.button("Comprobar archivos"):
        check_files()