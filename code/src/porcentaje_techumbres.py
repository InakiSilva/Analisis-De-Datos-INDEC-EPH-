from src.constants import AGLOMERADO_STR

def obtener_ultimo_trimestre(año, datos):
    """Obtiene el último trimestre disponible para un año específico."""
    filtro_por_anio = [fila for fila in datos if int(fila["ANO4"]) == año]
    if not filtro_por_anio:
        return None, None
    ultimo_trim = max(int(fila["TRIMESTRE"]) for fila in filtro_por_anio)
    datos_ultimo_trim = [fila for fila in filtro_por_anio if int(fila["TRIMESTRE"]) == ultimo_trim]
    return ultimo_trim, datos_ultimo_trim


def contar_hogares_por_aglomerado(datos_trimestre):
    """Cuenta hogares totales y con material precario por aglomerado."""
    aglomerados_stats = {}
    
    for hogar in datos_trimestre:
        aglomerado_codigo = hogar['AGLOMERADO']
        pondera = int(hogar['PONDERA'])
        
        # Inicializar el contador para este aglomerado si no existe
        if aglomerado_codigo not in aglomerados_stats:
            aglomerados_stats[aglomerado_codigo] = {'total': 0, 'precario': 0}
        
        # Sumar al total de hogares
        aglomerados_stats[aglomerado_codigo]['total'] += pondera
        
        # Verificar si el material del techo es precario
        if 'MATERIAL_TECHUMBRE' in hogar and hogar['MATERIAL_TECHUMBRE'] == 'Material precario':
            aglomerados_stats[aglomerado_codigo]['precario'] += pondera
            
    return aglomerados_stats


def calcular_porcentajes(aglomerados_stats):
    """Calcula el porcentaje de viviendas con material precario por aglomerado."""
    aglomerados_porcentajes = {}
    
    for aglomerado_codigo, datos in aglomerados_stats.items():
        if datos['total'] > 0:  # Evitar división por cero
            porcentaje = (datos['precario'] / datos['total']) * 100
            aglomerados_porcentajes[aglomerado_codigo] = porcentaje
            
    return aglomerados_porcentajes


def encontrar_extremos(aglomerados_porcentajes):
    """Encuentra los aglomerados con mayor y menor porcentaje."""
    if not aglomerados_porcentajes:
        return None, None, None, None
        
    # Encontrar el aglomerado con mayor porcentaje
    max_aglomerado_codigo = max(aglomerados_porcentajes, key=aglomerados_porcentajes.get)
    max_porcentaje = aglomerados_porcentajes[max_aglomerado_codigo]
    
    # Encontrar el aglomerado con menor porcentaje
    min_aglomerado_codigo = min(aglomerados_porcentajes, key=aglomerados_porcentajes.get)
    min_porcentaje = aglomerados_porcentajes[min_aglomerado_codigo]
    
    return max_aglomerado_codigo, max_porcentaje, min_aglomerado_codigo, min_porcentaje


def obtener_nombre_aglomerado(codigo):
    """Convierte código de aglomerado a nombre completo."""
    return AGLOMERADO_STR.get(int(codigo), f"Aglomerado {codigo}")


def analizar_material_precario(datos_hogares, year):
    """
    Función principal que coordina el análisis de material precario.
    
    Parámetros:
    - datos_hogares: Lista de diccionarios con datos de hogares
    - year: Año a analizar (como entero)
    
    Retorna:
    - Diccionario con los resultados del análisis o None si no hay datos.
    """
    # Convertir el año a entero si se pasa como string
    year = int(year)
    
    # Obtener datos del último trimestre del año seleccionado
    ultimo_trimestre, datos_ultimo_trimestre = obtener_ultimo_trimestre(year, datos_hogares)
    
    if not ultimo_trimestre:
        return {
            'año': year,
            'error': f"No hay datos disponibles para el año {year}"
        }
    
    # Contar hogares por aglomerado
    aglomerados_stats = contar_hogares_por_aglomerado(datos_ultimo_trimestre)
    
    # Calcular porcentajes
    aglomerados_porcentajes = calcular_porcentajes(aglomerados_stats)
    
    if not aglomerados_porcentajes:
        return {
            'año': year,
            'trimestre': ultimo_trimestre,
            'error': "No hay datos suficientes para calcular porcentajes de material precario."
        }
    
    # Encontrar extremos
    max_codigo, max_porcentaje, min_codigo, min_porcentaje = encontrar_extremos(aglomerados_porcentajes)
    
    if max_codigo and min_codigo:
        # Preparar resultado con nombres de aglomerados
        max_nombre = obtener_nombre_aglomerado(max_codigo)
        min_nombre = obtener_nombre_aglomerado(min_codigo)
        
        # Ordenar los porcentajes para facilitar su visualización
        porcentajes_ordenados = sorted(
            [(obtener_nombre_aglomerado(codigo), porcentaje) 
             for codigo, porcentaje in aglomerados_porcentajes.items()],
            key=lambda x: x[1],
            reverse=True
        )
        
        return {
            'año': year,
            'trimestre': ultimo_trimestre,
            'max_aglomerado_codigo': max_codigo,
            'max_aglomerado_nombre': max_nombre,
            'max_porcentaje': max_porcentaje,
            'min_aglomerado_codigo': min_codigo,
            'min_aglomerado_nombre': min_nombre,
            'min_porcentaje': min_porcentaje,
            'porcentajes_ordenados': porcentajes_ordenados
        }
    else:
        return {
            'año': year,
            'trimestre': ultimo_trimestre,
            'error': "No hay datos suficientes para calcular porcentajes de material precario."
        }

