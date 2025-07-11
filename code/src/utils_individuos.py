import pandas as pd
from src.constants import INDIVIDUAL_DATA_OUT_PATH

# ======== EJERCICIO 3A =============
GENEROS_STR = {1: "Masculino", 2: "Femenino"}
    
# ======== EJERCICIO 4A =============
NIVELES_EDUCATIVOS = {
    1: "Primario incompleto",
    2: "Primario completo",
    3: "Secundario incompleto",
    4: "Secundario completo",
}
# Evito repetir código
for nivel in [5,6]:
    NIVELES_EDUCATIVOS[nivel] = "Superior o universitario"
for nivel in [7,8,9]:
    NIVELES_EDUCATIVOS[nivel] = "Sin información" 

# ======== EJERCICIO 5A =============
def columna_CONDICION_LABORAL(estado, cat):
    '''
        Devuelve el valor de la nueva columna generada CONDICION_LABORAL a partir del los parametros estado y cat

        parametros :
            estado (integer) : Condición de actividad
                0 = Entrevista individual no realizada (no respuesta al cuestionario individual)
                1 = Ocupado
                2 = Desocupado
                3 = Inactivo
                4 = Menor de 10 años
            cat (integer) : Categoría ocupacional (Para ocupados y desocupados con ocupación anterior)
                1 = Patrón
                2 = Cuenta propia
                3 = Obrero o empleado
                4 = Trabajador familiar sin remuneración
                9 = Ns/Nr
            
        return
            - Ocupado autónomo: si ESTADO es igual a 1 y CAT_OCUP es 1 o 2. 
            - Ocupado dependiente: si ESTADO es igual a 1 y CAT_OCUP es 3 o 4 o 9. 
            - Desocupado: si ESTADO es igual a 2. 
            - Inactivo: si ESTADO es igual a 3. 
            - Fuera de categoría/sin información: si ESTADO es igual a 4.
            - pd.NA si faltan datos

    '''
    if pd.isna(estado) or (pd.isna(cat) and estado == 1):
        return pd.NA
    
    if estado == 2:
        return 'Desocupado'
    if estado == 3:
        return 'Inactivo'
    if estado == 4:
        return 'Fuera de categoría/sin información'
    if estado == 1:
        if cat in [1, 2]:
            # retorno segun la categoria
            return 'Ocupado autónomo'
        elif cat in [3, 4, 9]:
            return 'Ocupado dependiente' 
    return pd.NA
    
# ======== EJERCICIO 6A =============
def columna_UNIVERSITARIO(edad, nivel_ed):
    '''
        Devuelve el valor para la nueva columan generada llamada UNIVERSITARIO

        Parameters:
            edad (integer) : valor numerico referido a la edad
            nivel_ed (integer) : Nivel educativo
                1 = Primario incompleto (incluye educación especial)
                2 = Primario completo
                3 = Secundario incompleto
                4 = Secundario completo
                5 = Superior universitario incompleto
                6 = Superior universitario completo
                7 = Sin instrucción
                9 = Ns/Nr

        Returns: 
            Devuelve 1 si es mayor de edad (18+) y completó universidad (nivel 6)
            Devuelve 0 si es mayor pero no universitario completo, y 2 si es menor de edad.
            Devuelve 2 si no aplica
            Devuelve pd.NA si faltan datos
    '''
    # Se evalua que los valores no sean NaN
    if pd.isna(edad) or pd.isna(nivel_ed):
        return pd.NA
    
    # Se evalua el valor para la columna UNIVERSITARIO
    if edad < 18:
        return 2
    return 1 if nivel_ed == 6 else 0
    
# ======== FUNCION QUE CREA TODAS LAS COLUMNAS =============
COLUMNAS_DESEADAS = ["CH04", "CH06", "NIVEL_ED", "ESTADO", "CAT_OCUP"]

def create_columns_individuos():
    """
    Lee el CSV de individuos y calcula, agrega y escribe las columnas:
      - CH04_STR: Genero de la persona en formato str.
      - NIVEL_ED_str: Nivel de educación de la persona en formato str.
      - CONDICION_LABORAL: Condición laboral de la persona.
      - UNIVERSITARIO: Indica si la persona es mayor con titulo universitario, sin titulo o no aplica.
    """
    
    # Abrir el archivo
    df = pd.read_csv(INDIVIDUAL_DATA_OUT_PATH,delimiter=';')

    # Convertir todas las columnas a numeros una sola vez
    df[COLUMNAS_DESEADAS] = df[COLUMNAS_DESEADAS].apply(pd.to_numeric, errors='coerce')

    # COLUMNA CH04_STR
    df['CH04_STR'] = df['CH04'].map(GENEROS_STR)

    # COLUMNA NIVEL_ED_str
    df['NIVEL_ED_str'] = df['NIVEL_ED'].map(NIVELES_EDUCATIVOS)

    # COLUMNA CONDICION_LABORAL
    df['CONDICION_LABORAL'] = df.apply(lambda row: columna_CONDICION_LABORAL(row.ESTADO,row.CAT_OCUP),axis=1)

    # COLUMNA UNIVERSITARIO
    df['UNIVERSITARIO'] = df.apply(lambda row: columna_UNIVERSITARIO(row.CH06,row.NIVEL_ED),axis=1)
    
    # Escribir columnas nuevas en el archivo 
    df.to_csv(INDIVIDUAL_DATA_OUT_PATH, index=False, sep=';')
