from pathlib import Path

# Ruta base del proyecto
ROOT_DIRECTORY = Path(__file__).resolve().parent.parent

# Ruta de la carpeta 'files'
FILES_DIRECTORY = ROOT_DIRECTORY / 'files'

# Ruta de la carpeta 'hogares' dentro de 'files'
FILES_HOGARES_DIRECTORY = FILES_DIRECTORY / 'hogares'

# Ruta de la carpeta 'Individuos' dentro de 'files'
FILES_INDIVIDUOS_DIRECTORY = FILES_DIRECTORY / 'individuos'

# Ruta del archivo con valores de la canasta básica
CANASTA_FILE_PATH = FILES_DIRECTORY / 'valores-canasta-basica-alimentos-canasta-basica-total-mensual-2016.csv'

# Ruta del archivo de salida del ejercicio 2
DATA_OUT_PATH = ROOT_DIRECTORY / 'data_out'

# Ruta del archivo de salida de individuos
INDIVIDUAL_DATA_OUT_PATH = DATA_OUT_PATH / 'usus_individual.csv'

# Ruta del archivo de salida de hogares
HOGAR_DATA_OUT_PATH = DATA_OUT_PATH / 'usus_hogar.csv'

# Ruta al archivo aglomerado coordenadas
FILE_AGLOMERADO_COORDENADAS = FILES_DIRECTORY / "aglomerados_coordenadas.json"

FILE_RANKING_CINCO_AGLOMERADOS = DATA_OUT_PATH / "ranking_aglomerados.csv"

# Codigo de administracion de actividad
ADMINISTRACION_ACTIVIDAD = {
    1 : "Estatal",
    2 : "Privado",
    3 : "Otra"
}

# Codigo de aglomerado correspondiente a su nombre 
AGLOMERADO_STR = {
    2: 'Gran La Plata',
    3: 'Bahía Blanca - Cerri',
    4: 'Gran Rosario',
    5: 'Gran Santa Fé',
    6: 'Gran Paraná',
    7: 'Posadas',
    8: 'Gran Resistencia',
    9: 'Comodoro Rivadavia - Rada Tilly',
    10: 'Gran Mendoza',
    12: 'Corrientes',
    13: 'Gran Córdoba',
    14: 'Concordia',
    15: 'Formosa',
    17: 'Neuquén – Plottier',
    18: 'Santiago del Estero - La Banda',
    19: 'Jujuy - Palpalá',
    20: 'Río Gallegos',
    22: 'Gran Catamarca',
    23: 'Gran Salta',
    25: 'La Rioja',
    26: 'Gran San Luis',
    27: 'Gran San Juan',
    29: 'Gran Tucumán - Tafí Viejo',
    30: 'Santa Rosa – Toay',
    31: 'Ushuaia - Río Grande',
    32: 'Ciudad Autónoma de Buenos Aires',
    33: 'Partidos del GBA',
    34: 'Mar del Plata',
    36: 'Río Cuarto',
    38: 'San Nicolás – Villa Constitución',
    91: 'Rawson – Trelew',
    93: 'Viedma – Carmen de Patagones'
}
