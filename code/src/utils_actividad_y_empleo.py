import streamlit as st
import pandas as pd
import json
import folium
from constants import AGLOMERADO_STR, ADMINISTRACION_ACTIVIDAD, FILE_AGLOMERADO_COORDENADAS
from streamlit_folium import st_folium
from obtener_fechas import streamlit_get_quarters_range


def desocupacion_por_nivel_ed(df, anio, trimestre):
    """
        Muestra la cantidad de personas desocupadas agrupadas por nivel educativo
        para un año y trimestre específicos.

        Parámetros:
            df (pandas.DataFrame): DataFrame que contiene los datos individuales de empleo y desempleo, debe incluir las columnas 'ANO4', 'TRIMESTRE', 'CONDICION_LABORAL','NIVEL_ED_str' y 'PONDERA'.
            anio (int): Año para filtrar los datos (columna 'ANO4').
            trimestre (int): Trimestre para filtrar los datos (columna 'TRIMESTRE').
    """

    st.header("Desocupación por nivel educativo")

    # Filtro las filas del archivo que coinciden con el año y trimeste ingresado y con condicion laboral desocupado
    filtrado = df[(df["ANO4"] == anio) & (df["TRIMESTRE"] == trimestre) & (
        df["CONDICION_LABORAL"] == "Desocupado")]

    # Cuento cuantas personas hay para cada nivel educativo
    conteo = filtrado.groupby("NIVEL_ED_str")["PONDERA"].sum()
    conteo = conteo.reset_index()
    conteo.columns = ["Nivel educativo", "Cantidad de personas"]

    st.markdown("### 📋 Personas desocupadas por nivel educativo")
    st.dataframe(conteo, use_container_width=True, hide_index=True)


def tasa_desempleo_empleo(df, columnasAgrupadas, retornar_tasa_empleo=False,):
    """
        Calcula la tasa de desempleo o empleo a partir de un DataFrame. Agrupa los datos según las columnas especificadas, 
        filtra a las personas ocupadas y desocupadas, y luego calcula la tasa correspondiente según el parámetro `retornar_tasa_empleo`

        Parámetros:
            df : pandas.DataFrame
            DataFrame con los datos individuales, debe contener las columnas "CONDICION_LABORAL" y "PONDERA".

            columnasAgrupadas : str o list de str
            Columna o columnas por las cuales se agruparán los datos.

            retornar_tasa_empleo : boolean, opcional (por defecto: False)
            Si es True, retorna la tasa de empleo. Si es False, retorna la tasa de desempleo.

        Retorna : pandas.DataFrame
            DataFrame con las columnas agrupadas y una columna adicional:
                - "Tasa de empleo" si `retornar_tasa_empleo` es True.
                - "Tasa de desempleo" si `retornar_tasa_empleo` es False.

    """

    # Filtro desocupados
    desocupados = df[(df["CONDICION_LABORAL"] == "Desocupado") | (
        df["CONDICION_LABORAL"] == "Inactivo") | (df["CONDICION_LABORAL"] == "Fuera de categoría/sin información")]

    # Filtro ocupados
    ocupados = df[(df["CONDICION_LABORAL"] == "Ocupado dependiente") | (
        df["CONDICION_LABORAL"] == "Ocupado autónomo")]

    # Agrupo y sumo los valores de la columna "PONDERA"
    desocupados_agrupados = desocupados.groupby(columnasAgrupadas)[
        "PONDERA"].sum()

    ocupados_agrupados = ocupados.groupby(columnasAgrupadas)["PONDERA"].sum()

    if (retornar_tasa_empleo):
        # Calculo la tasa de empleo
        tasa_empleo = (ocupados_agrupados /
                       (desocupados_agrupados + ocupados_agrupados)) * 100
        tasa_empleo_df = tasa_empleo.reset_index(name="Tasa de empleo")
        return tasa_empleo_df
    else:
        # Calculo la tasa de desempleo
        tasa_desempleo = (desocupados_agrupados /
                          (desocupados_agrupados + ocupados_agrupados)) * 100
        tasa_desempleo_df = tasa_desempleo.reset_index(
            name="Tasa de desempleo")
        return tasa_desempleo_df


def evolucion_desempleo_empleo(df):
    """
        Grafica la evolución temporal de la tasa de empleo y desempleo, 
        ya sea a nivel nacional o para un aglomerado específico.

        Parámetros:
            df : pandas.DataFrame
                DataFrame proveniente del archivo 'usu_individual.csv', que debe contener 
                las siguientes columnas:
                - 'AGLOMERADO': Código numérico del aglomerado geográfico.
                - 'CONDICION_LABORAL': Estado laboral de cada persona (ocupado, desocupado, etc.).
                - 'ANO4': Año del relevamiento.
                - 'TRIMESTRE': Trimestre del relevamiento.
                - 'PONDERA': Cantidad de valores ponderados.

    """

    st.header("📈 Evolución del empleo y desempleo")

    aglomerados = df["AGLOMERADO"].unique()
    # Creacion de un diccionario que asocia el nombre del aglomerado con su código
    nombre_aglomerados = {AGLOMERADO_STR[cod]: cod for cod in aglomerados}
    # Creacion de un menú desplegable para que el usuario elija un aglomerado o todo el país
    aglomerado_seleccionado = st.selectbox("🌍 Filtrar por : ", options=[
                                           "Todo el pais"] + list(nombre_aglomerados.keys()))
    aglomerado_seleccionado = str(aglomerado_seleccionado)

    # Filtro el archivo en base al aglomerado elegido
    if aglomerado_seleccionado == "Todo el pais":
        df_filtrado = df.copy()
    else:
        cod_aglomerado = nombre_aglomerados[aglomerado_seleccionado]
        df_filtrado = df[df["AGLOMERADO"] == cod_aglomerado]

    tasa_desempleo_df = tasa_desempleo_empleo(
        df_filtrado, ["ANO4", "TRIMESTRE"])
    tasa_empleo_df = tasa_desempleo_empleo(
        df_filtrado, ["ANO4", "TRIMESTRE"], True)

    # Uno los dos DataFrames por año y trimestre
    tasas_df = pd.merge(tasa_desempleo_df, tasa_empleo_df,
                        on=["ANO4", "TRIMESTRE"])

    # Creo una columna "Fecha" para el índice
    tasas_df["Fecha"] = tasas_df["ANO4"].astype(
        str) + " T" + tasas_df["TRIMESTRE"].astype(str)
    tasas_df = tasas_df.set_index("Fecha")

    st.line_chart(tasas_df[["Tasa de desempleo", "Tasa de empleo"]],
                  x_label="Fecha", y_label="Tasa (%)", color=("#FF0000", "#00CC00"))


def informacion_ocupacion_por_aglomerado(df):
    """
        Muestra una tabla con el total de personas ocupadas y el porcentaje de empleo estatal, 
        privado y de otro tipo para cada aglomerado, utilizando los datos de ocupación principal.

        Parámetros:
            df : pandas.DataFrame
                DataFrame que contiene información individual de personas, incluyendo las columnas:
                - 'CONDICION_LABORAL': Indica si la persona está ocupada y su tipo de empleo.
                - 'PP04A': Código que representa el tipo de administración (privada, estatal, otra).
                - 'AGLOMERADO': Código del aglomerado geográfico.
                - 'PONDERA': Cantidad de datos ponderados.

    """

    st.header("👷 Informacion de empleo por aglomerado")

    # Filtro ocupados
    df_filtrados = df[(df["CONDICION_LABORAL"] == "Ocupado dependiente") | (
        df["CONDICION_LABORAL"] == "Ocupado autónomo")]

    # Agrupo por aglomerado y por categoria de ocupacion (privada/estatal/otra)
    ocupados_agrupados = df_filtrados.groupby(["AGLOMERADO", "PP04A"])[
        "PONDERA"].sum().reset_index(name="Total")

    # Total de ocupados por aglomerado
    totales_aglomerado = ocupados_agrupados.groupby(
        "AGLOMERADO")["Total"].sum().reset_index(name="Total ocupados")

    # Merge para tener el total en cada fila
    ocupados_con_totales = ocupados_agrupados.merge(
        totales_aglomerado, on="AGLOMERADO")

    # Calcular porcentaje
    ocupados_con_totales["Porcentaje"] = 100 * \
        ocupados_con_totales["Total"] / ocupados_con_totales["Total ocupados"]

    # Cambio el nombre de las columnas
    ocupados_con_totales.columns = [
        "Aglomerado", "Administracion", "Total personas", "Total ocupados", "Porcentaje"]

    # En lugar de mostrar los codigos del aglomerado y administracion muestro sus equivalentes a string
    ocupados_con_totales["Aglomerado"] = ocupados_con_totales["Aglomerado"].map(
        AGLOMERADO_STR)
    ocupados_con_totales["Administracion"] = ocupados_con_totales["Administracion"].map(
        ADMINISTRACION_ACTIVIDAD)

    # Pivot para mostrar un aglomerado por fila y los tipos de administración como columnas
    tabla_pivot = ocupados_con_totales.pivot_table(
        index=["Aglomerado", "Total ocupados"],
        columns="Administracion",
        values="Porcentaje"
    ).reset_index()

    # Renombro las columnas
    tabla_pivot.columns.name = None
    tabla_pivot = tabla_pivot.rename(columns={
        "Estatal": "Estatal (%)",
        "Privada": "Privada (%)",
        "Otra": "Otra (%)"
    })

    st.dataframe(tabla_pivot, use_container_width=True, hide_index=True)


def generate_map():
    attr = (
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
        'contributors, &copy; <a href="https://cartodb.com/attributions">CartoDB</a>'
    )

    tiles = 'https://wms.ign.gob.ar/geoserver/gwc/service/tms/1.0.0/capabaseargenmap@EPSG%3A3857@png/{z}/{x}/{-y}.png'
    m = folium.Map(
        location=(-33.457606, -65.346857),
        control_scale=True,
        zoom_start=5,
        name='es',
        tiles=tiles,
        attr=attr
    )
    return m


def aglomerado_mapa_empleo_desempleo(df):

    '''
        Visualiza en un mapa interactivo la evolución de las tasas de empleo y desempleo por aglomerado
        entre el trimestre más antiguo y el más reciente disponibles en el DataFrame.

        La función muestra un encabezado, las fechas de inicio y fin del análisis, y permite al usuario 
        seleccionar mediante toggles si desea visualizar la tasa de empleo o desempleo. 
        Los puntos en el mapa representan los distintos aglomerados y están coloreados de acuerdo al 
        comportamiento de la tasa: verde para mejora (mayor empleo o menor desempleo) y rojo para empeora 
        (menor empleo o mayor desempleo). Cada punto tiene un *popup* con información de las tasas de inicio y fin.

        Parámetros:
        df : pandas.DataFrame
            DataFrame con los datos de la EPH, debe contener las columnas 'ANO4', 'TRIMESTRE',
            'AGLOMERADO' y 'CONDICION_LABORAL'.
    '''

    st.header("📍 Evolución de tasa de empleo y desempleo por aglomerado")

    # Cargar coordenadas desde JSON
    with open(FILE_AGLOMERADO_COORDENADAS, "r") as f:
        coords_json = json.load(f)

    rango_fechas = streamlit_get_quarters_range()
    fecha_mas_antigua = rango_fechas[0]
    fecha_mas_actual = rango_fechas[1]

    st.info(
        f"Informacion desde {fecha_mas_antigua[0]}/{fecha_mas_antigua[1]} hasta {fecha_mas_actual[0]}/{fecha_mas_actual[1]}")

    st.markdown("### ⚙️ Filtros ")

    tasa = st.segmented_control("Seleccione la tasa : ", options=["Tasa desempleo", "Tasa empleo"])

    df_inicio = df[(df["ANO4"] == fecha_mas_antigua[0]) &
                   (df["TRIMESTRE"] == fecha_mas_antigua[1])]
    df_fin = df[(df["ANO4"] == fecha_mas_actual[0]) &
                (df["TRIMESTRE"] == fecha_mas_actual[1])]

    mapa = generate_map()

    # Mostrar tasa de empleo
    if tasa == "Tasa empleo":
        tasa_inicio = tasa_desempleo_empleo(df_inicio, ["AGLOMERADO"], True)
        tasa_fin = tasa_desempleo_empleo(df_fin, ["AGLOMERADO"], True)
        tasa_inicio = tasa_inicio.rename(columns={"Tasa de empleo": "tasa_inicio"})
        tasa_fin = tasa_fin.rename(columns={"Tasa de empleo": "tasa_fin"})
        comparacion = pd.merge(tasa_inicio, tasa_fin, on="AGLOMERADO")
        comparacion["aumento"] = comparacion["tasa_fin"] > comparacion["tasa_inicio"]
        comparacion = comparacion.set_index("AGLOMERADO")

        for aglo_id, fila in comparacion.iterrows():
            aglo_id_str = str(aglo_id)
            coords = coords_json[aglo_id_str]["coordenadas"]
            nombre = coords_json[aglo_id_str]["nombre"]
            if fila["aumento"]:
                color = "green"
            else:
                color = "red"
            folium.CircleMarker(
                location=coords,
                radius=6,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.8,
                popup=f"[EMPLEO] {nombre}: {fila['tasa_inicio']:.2f}% → {fila['tasa_fin']:.2f}%"
            ).add_to(mapa)

    # Mostrar tasa de desempleo
    if tasa == "Tasa desempleo":
        tasa_inicio = tasa_desempleo_empleo(df_inicio, ["AGLOMERADO"])
        tasa_fin = tasa_desempleo_empleo(df_fin, ["AGLOMERADO"])
        tasa_inicio = tasa_inicio.rename(columns={"Tasa de desempleo": "tasa_inicio"})
        tasa_fin = tasa_fin.rename(columns={"Tasa de desempleo": "tasa_fin"})
        comparacion = pd.merge(tasa_inicio, tasa_fin, on="AGLOMERADO")
        comparacion["aumento"] = comparacion["tasa_fin"] > comparacion["tasa_inicio"]
        comparacion = comparacion.set_index("AGLOMERADO")

        for aglo_id, fila in comparacion.iterrows():
            aglo_id_str = str(aglo_id)
            coords = coords_json[aglo_id_str]["coordenadas"]
            nombre = coords_json[aglo_id_str]["nombre"]
            if fila["aumento"]:
                color = "red"
            else:
                color = "green"
            folium.CircleMarker(
                location=coords,
                radius=6,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.8,
                popup = f"[DESEMPLEO] {nombre}: {fila['tasa_inicio']:.2f}% → {fila['tasa_fin']:.2f}%"
            ).add_to(mapa)

    # Mostrar mapa en Streamlit
    st_folium(mapa, width=700, height=500)
