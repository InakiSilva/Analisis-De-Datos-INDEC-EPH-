from src.constants import AGLOMERADO_STR, INDIVIDUAL_DATA_OUT_PATH, HOGAR_DATA_OUT_PATH, FILE_RANKING_CINCO_AGLOMERADOS
from src.obtener_fechas import get_latest_quarter
import pandas as pd
import os
from pathlib import Path


def calcular_datos_hogares_por_aglomerado ():

    """
    Calcula los 5 aglomerados con mayor proporción de hogares que 
    tienen al menos dos personas con educación superior o universitaria completa.

    El análisis se realiza a partir de los datos más recientes disponibles en los 
    archivos procesados de hogares e individuos. La función filtra los registros por 
    trimestre y año actual, identifica los hogares que cumplen la condición educativa 
    y calcula el porcentaje correspondiente sobre el total de hogares de cada aglomerado.

    Returns:
        pd.DataFrame: Un DataFrame con dos columnas:
            - 'Aglomerado': nombre del aglomerado (según mapeo AGLOMERADO_STR)
            - 'porcentaje': porcentaje de hogares con ≥2 universitarios respecto al total
    """

    df_hogares = pd.read_csv(HOGAR_DATA_OUT_PATH , delimiter=';')
    df_individuos = pd.read_csv(INDIVIDUAL_DATA_OUT_PATH, delimiter=';')

    fecha_mas_actual = get_latest_quarter()

    # Filtrar hogares por año y trimestre
    hogares_filtrados = df_hogares[
        (df_hogares["ANO4"] == fecha_mas_actual[0]) &
        (df_hogares["TRIMESTRE"] == fecha_mas_actual[1])
    ]   

    # Filtrar individuos por año y trimestre
    individuos_filtrados = df_individuos[
        (df_individuos["ANO4"] == fecha_mas_actual[0]) &
        (df_individuos["TRIMESTRE"] == fecha_mas_actual[1])
    ]

    # Filtrar individuos con educación superior
    universitarios = individuos_filtrados[individuos_filtrados["NIVEL_ED_str"] == "Superior o universitario"]

    # Contar universitarios por hogar
    universitarios_por_hogar = universitarios.groupby(["CODUSU", "NRO_HOGAR"]).size().reset_index(name="universitarios")

    # Identificar hogares con 2 o más universitarios
    hogares_con_2_o_mas = universitarios_por_hogar[universitarios_por_hogar["universitarios"] >= 2]

    # Unir con hogares filtrados para obtener info de aglomerado y pondera
    hogares_con_2_o_mas_info = hogares_filtrados.merge(hogares_con_2_o_mas, on=["CODUSU", "NRO_HOGAR"])

    # Sumar PONDERA de hogares con 2+ universitarios por aglomerado
    ponderados_2plus = hogares_con_2_o_mas_info.groupby("AGLOMERADO")["PONDERA"].sum().reset_index(name="hogares_2habit_pond")

    # Sumar PONDERA total de hogares por aglomerado
    total_ponderados = hogares_filtrados.groupby("AGLOMERADO")["PONDERA"].sum().reset_index(name="total_pondera")

    # Unir y calcular porcentaje ponderado
    ranking = total_ponderados.merge(ponderados_2plus, on="AGLOMERADO", how="left")
    ranking["hogares_2habit_pond"] = ranking["hogares_2habit_pond"].fillna(0)
    ranking["porcentaje"] = 100 * ranking["hogares_2habit_pond"] / ranking["total_pondera"]

    # Mapear nombres de aglomerados
    ranking["Aglomerado"] = ranking["AGLOMERADO"].map(AGLOMERADO_STR)

    # Obtener top 5
    top_5 = ranking.sort_values("porcentaje", ascending=False).head(5)

    return top_5[["Aglomerado", "porcentaje"]]


def guardar_ranking_aglomerados(top_5):
    """
    Guarda el DataFrame con el ranking de los cinco aglomerados con mayor proporción 
    de hogares con al menos dos personas con educación superior en un archivo CSV.

    Args:
        top_5 (pd.DataFrame): DataFrame que contiene las columnas 'Aglomerado' y 'porcentaje'

    Returns:
        pd.DataFrame: El mismo DataFrame recibido como entrada, sin modificaciones.
    """

    # Ruta absoluta del archivo de salida
    print(f"Intentando guardar en: {FILE_RANKING_CINCO_AGLOMERADOS}")

    # Guardar el CSV
    top_5.to_csv(FILE_RANKING_CINCO_AGLOMERADOS, index=False)
    print(f"CSV guardado en: {FILE_RANKING_CINCO_AGLOMERADOS}")

    return top_5
