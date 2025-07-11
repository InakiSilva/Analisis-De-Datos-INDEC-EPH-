import pandas as pd
from src.constants import HOGAR_DATA_OUT_PATH

# ======== EJERCICIO 7A =============
def columna_tipo_hogar(ix_tot):
    '''
    Devuelve el tipo de hogar (unipersonal, nuclear, extendido), en base al parametro ix_tot

    Parametro
        ix_tot (integer) : cantidad total de miembros del hogar

    return 
        'Unipersonal' : si ix_tot es igual a 1
        'Nuclear' : si ix_tot esta entre 2 y 4
        'Extendido' : si ix_tot es mayor e igual que 5
    '''
    # Se evalua que el valor no sea NaN
    if pd.isna(ix_tot):
        return pd.NA
    
    # Se evalua el tipo de hogar
    if ix_tot == 1:
        return 'Unipersonal'
    elif 2 <= ix_tot <= 4:
        return 'Nuclear'
    else:
        return 'Extendido'

# ======== EJERCICIO 8A =============
def columna_material_techumbre(iv4):
    '''
    Devuelve el valor para la nueva columna MATERIAL_TECHUMBRE, en base a el campo iv4

    Parametro
        iv4 (integer): La cubierta exterior del techo es de : 
            1. membrana / cubierta asfáltica
            2. baldosa / losa sin cubierta
            3. pizarra / teja
            4. chapa de metal sin cubierta
            5. chapa de fibrocemento / plástico
            6. chapa de cartón
            7. saña / tabla / paja con barro / paja sola
            9. N/S. Departamento en propiedad horizontal

    return 
        'Material precario' : si iv4 esta entre 5 y 7
        'Material durable' : si iv4 esta entre 1 y 4
        'No aplica' : si iv4 es 9  
    '''
    # Se evalua que el valor no sea NaN
    if pd.isna(iv4):
        return pd.NA

    # Se el material
    if iv4 >= 1 and iv4 <= 4:
        return 'Material durable'
    elif iv4 >= 5 and iv4 <= 7:
        return 'Material precario'
    elif iv4 == 9:
        return 'No aplica'
    return pd.NA

# ======== EJERCICIO 9A =============
def columna_densidad_hogar(v2, ix_tot):
    '''
    Devuelve la densidad del hogar (bajo, medio, alto) en base al parametro V2 (cantidad de habitaciones) y al parametro ix_tox (cantidad total de miembros del hogar)

    Parametros:
        V2 (integer): cantidad de habitaciones
        ix_tox (integer): cantidad total de miembros del hogar

    Returns:
        * Bajo: menos de 1 persona por habitación.
        * Medio: entre 1 y 2 personas por habitación
        * Alto: más de 2 personas por habitación.
    '''
    # Se evalua que los valores no sean NaN
    if pd.isna(v2) or pd.isna(ix_tot) or ix_tot == 0:
        return pd.NA

    # Se evalua la densidad
    valor = v2 / ix_tot
    if valor >= 0 and valor < 1:
        return 'Bajo'
    elif valor >= 1 and valor <= 2:
        return 'Medio'
    elif valor > 2:
        return 'Alto'
    return pd.NA

# ======== EJERCICIO 10A =============
def calificar_condicion(iv6, iv7, iv8, iv9, iv10):
    """
    Devuelve la condicion de habitabilidad de la vivienda recibida como parametro:

    Categorías:
    - Insuficiente: agua fuera del terreno, agua con bomba manual u otra fuente desconocida, baño fuera del terreno o inexistente.
    - Regular: agua fuera de la vivienda pero dentro del terreno, baño fuera de la vivienda pero dentro del terreno, o baño letrina.
    - Saludables: agua por cañería dentro de la vivienda con bomba a motor, o baño dentro de la vivienda con inodoro sin botón / cadena y con arrastre de agua (a balde).
    - Buena: agua por cañería dentro de la vivienda y de red pública, o baño dentro de la vivienda con inodoro con botón / mochila / cadena y arrastre de agua.

    Parameters:
        iv6 : Tiene agua por : (1) cañería dentro de la vivienda, (2)fuera de la vivienda pero dentro del terreno, (3) fuera del terreno
        iv7 : El agua es de : (1) red pública (agua corriente), (2) perforación con bomba a motor, (3) perforación con bomba manual
        iv8 : ¿Tiene baño / letrina ?  : (1) Sí, (2) No
        iv9 : El baño o letrina está : 1)dentro de la vivienda, (2) fuera de la vivienda, pero dentro del terreno, (3) fuera del terreno
        iv10 : El baño tiene : (1) inodoro con botón / mochila / cadena y arrastre de agua, (2) inodoro sin botón / cadena y con arrastre de agua (a balde), (3) letrina (sin arrastre de agua)

    Returns:
        str: La condicion de habitabilidad de la vivienda.
    """  
    # Se evalua que los valores no sean NaN
    if any(pd.isna([iv6, iv7, iv8, iv9, iv10])):
        return pd.NA

    # Se evalua la condicion de habitabilidad
    if iv6 == 3 or iv7 >= 3 or iv8 == 2 or iv9 == 3:
        return 'insuficiente'
    if iv6 == 2 or iv9 == 2 or iv10 == 3:
        return 'regular'
    if (iv6 == 1 and iv7 == 2) or (iv9 == 1 and iv10 == 2):
        return 'saludables'
    if (iv6 == 1 and iv7 == 1) or (iv9 == 1 and iv10 == 1):
        return 'buena'
    return pd.NA

# ======== FUNCION QUE CREA TODAS LAS COLUMNAS =============
COLUMNAS_DESEADAS = ['IX_TOT', 'IV4', 'V2','IV6','IV7','IV8','IV9','IV10']

def create_columns_hogares():
    """
    Lee el CSV de hogares y calcula, agrega y escribe las columnas:
      - TIPO_HOGAR: Tipo de hogar en formato str, puede ser 'Unipersonal', 'Nuclear', 'Extendido, o pd.NA si no hay datos.
      - MATERIAL_TECHUMBRE: Clasificación de la cubierta exterior del techo segun su material, puede ser:
        1. 'Material precario'
        2. 'Material durable'
        3. 'No aplica'
        4. o pd.NA si no hay datos.
      - DENSIDAD_HOGAR: Densidad del hogar, puede ser bajo, medio, alto o pd.NA si no hay datos.
      - CONDICION_DE_HABITABILIDAD: Condicion de habitabilidad de la vivienda, puede ser:
        1. 'Insuficiente'
        2. 'Regular'
        3. 'Saludables'
        4. 'Buena'
        5. o pd.NA si no hay datos.
      
    """
    
    # Abrir el archivo
    df = pd.read_csv(HOGAR_DATA_OUT_PATH,delimiter=';')

    # Convertir todas las columnas a numeros una sola vez
    df[COLUMNAS_DESEADAS] = df[COLUMNAS_DESEADAS].apply(pd.to_numeric, errors='coerce')

    # Columna TIPO_HOGAR
    df['TIPO_HOGAR'] = df['IX_TOT'].map(columna_tipo_hogar)

    # Columna MATERIAL_TECHUMBRE
    df['MATERIAL_TECHUMBRE'] = df['IV4'].map(columna_material_techumbre)

    # Columna DENSIDAD_HOGAR
    df['DENSIDAD_HOGAR'] = df.apply(lambda row: columna_densidad_hogar(row.V2, row.IX_TOT), axis=1)

    # Columna CONDICION_DE_HABITABILIDAD
    df['CONDICION_DE_HABITABILIDAD'] = df.apply(
        lambda row: calificar_condicion(row.IV6, row.IV7, row.IV8, row.IV9, row.IV10), axis=1
    )
     
    # Escribir columnas nuevas en el archivo 
    df.to_csv(HOGAR_DATA_OUT_PATH, index=False, sep=';')