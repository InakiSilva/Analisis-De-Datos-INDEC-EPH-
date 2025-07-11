
from src.constants import FILES_HOGARES_DIRECTORY, FILES_INDIVIDUOS_DIRECTORY
import streamlit as st


def add_quarter(file_name, quarters, file_type):
    """
    Comprueba si el nombre de un archivo sigue el formato usu_{file_type}_TQYY.txt, siendo file_type el tipo de archivo a buscar 
    (por ejemplo, "hogar" o "individual"), Q un número de trimestre entre 1 y 4 y YY un número de año con 2 dígitos. 
    Extrae el año y el trimestre y lo almacena como una tupla en el conjunto quarters, recibido como parametro.

    Params:
        file_name (str): Nombre del archivo a evaluar.
        quarters (set): Conjunto que almacena tuplas para cada trimestre en el formato (año, trimestre).
        file_type (str): Tipo de archivo buscado en el nombre (usado para la validación).
    """
    # Verifica que el nombre cumple con el patrón básico
    if file_name.startswith(f"usu_{file_type}_T") and file_name.endswith(".txt"):
        splited_name = file_name.split('_T')
        # Se verifica que al separar por _T queden 2 elementos y el segundo tenga 7 caracteres (ejemplo: "224.txt")
        if len(splited_name) == 2 and len(splited_name[1]) == 7:
            name_date = splited_name[1]
            quarter = name_date[0]
            year = name_date[1:3]

            # Comprueba que el nombre no tenga un formato distinto
            if quarter.isnumeric() and year.isnumeric():
                quarter = int(quarter)
                year = 2000 + int(year)
                if(1 <= quarter <= 4):
                    quarters.add((year, quarter))

def get_quarters(file_type='ambos'):
    """
    Recorre los archivos de las carpetas indicadas, extrae del nombre de cada archivo 
    el año y el trimestre, y retorna un conjunto con todos los pares (año, trimestre) encontrados.

    Params:
        file_type (str, optional): 'hogar' para procesar solo hogares, 'individual' para solo individuos, 
              o 'ambos' para ambos directorios. Por defecto es 'ambos'.

    Returns:
        set: Conjunto de tuplas (año, trimestre).
    """

    # Se declara la estructura para almacenar trimestres
    quarters = set()

    # Se recorren los archivos en la carpeta de hogares
    if file_type in ('hogar', 'ambos'):
        for file in FILES_HOGARES_DIRECTORY.iterdir():
            add_quarter(file.name,quarters,'hogar')

    # Se recorren los archivos en la carpeta de individuos
    if file_type in ('individual', 'ambos'):
        for file in FILES_INDIVIDUOS_DIRECTORY.iterdir():
            add_quarter(file.name,quarters,'individual')

    return quarters

def get_quarters_range(file_type='ambos'):
    """
    Obtiene el año y trimestre mas antiguo y mas actual de los archivos disponibles en las carpetas indicadas 
    y retorna como una tupla de tuplas
    Params:
        file_type (str, optional): 'hogar' para procesar solo hogares, 'individual' para solo individuos, 
              o 'ambos' para ambos directorios. Por defecto es 'ambos'.
    Returns:
        tuple,None: Tupla con el trimestre mas antigüo y mas actual con formato ((añoMin, trimestreMin), (añoMax, trimestreMax)) o None si no hay archivos
        en la/s carpetas especificadas
    """
    quarters = get_quarters(file_type=file_type)
    if quarters:
        first_quarter = min(quarters)
        last_quarter = max(quarters)
        return (first_quarter, last_quarter)
    else:
        return None
    
def get_latest_quarter(file_type='ambos'):
    """
    Devuelve el trimestre más reciente de los archivos disponibles.

    Params:
        file_type (str, optional): 'hogar' para procesar solo hogares, 'individual' para solo individuos, 
              o 'ambos' para ambos directorios. Por defecto es 'ambos'.
    Returns:
        tuple,None: Tupla con el trimestre mas actual con formato (añoMax, trimestreMax) o None si no hay archivos
        en la/s carpetas especificadas
    """
    quarters = get_quarters(file_type)
    return max(quarters) if quarters else None

# ======= UTILIDADES DE OBTENER FECHAS PARA STREAMLIT ============

def streamlit_get_quarters(file_type='ambos'):
    """
    Llama a get_quarters y muestra errores en Streamlit si faltan la carpeta o permisos.

    Params:
        file_type (str, optional): 'hogar' para procesar solo hogares, 'individual' para solo individuos, 
              o 'ambos' para ambos directorios. Por defecto es 'ambos'.
    Returns:
        set: Conjunto de tuplas (año, trimestre).
    """
    if file_type == 'ambos':
        folders = 'hogares o individuos'
    else:
        folders = 'hogares' if file_type == 'hogar' else 'individuos'
    try:
        return get_quarters(file_type)
    except FileNotFoundError:
        st.error(f"No existe la carpeta {folders}.")
        st.stop()
    except PermissionError:
        st.error(f"No tienes permiso para acceder a la carpeta {folders}.")
        st.stop()


def streamlit_get_quarters_range(file_type='ambos'):
    """
    Llama a get_quarters_range y muestra errores en Streamlit si faltan la carpeta o permisos.

    Params:
        file_type (str, optional): 'hogar' para procesar solo hogares, 'individual' para solo individuos, 
              o 'ambos' para ambos directorios. Por defecto es 'ambos'.
    Returns:
        Tuple,None: ((año_min, trim_min), (año_max, trim_max)) o None si no hay archivos.
    """
    if file_type == 'ambos':
        folders = 'hogares o individuos'
    else:
        folders = 'hogares' if file_type == 'hogar' else 'individuos'
    try:
        return get_quarters_range(file_type)
    except FileNotFoundError:
        st.error(f"No existe la carpeta {folders}.")
        st.stop()
    except PermissionError:
        st.error(f"No tienes permiso para acceder a la carpeta {folders}.")
        st.stop()