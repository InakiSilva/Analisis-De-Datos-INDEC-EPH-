import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from constants import AGLOMERADO_STR  

#-------------
#Funcoin para el ejercicio 1.3.1
#----------------


def distribucion_por_edad_y_sexo(df):
    """ El usuario selecciona un año y un trimestre.
        Se muestra un gráfico de barras dobles con la distribución de la población
        por grupos de edad de 10 años y por sexo.
    """

    st.header("Distribución por grupos de edad y sexo")
    st.markdown("Se muestra la distribución de la poblacion agrupada por rangos de edad y por género")

    #  lectura del año 
    anos_disponibles = sorted(df["ANO4"].unique())
    anio = st.selectbox("Seleccione el año:", anos_disponibles, key="anio_2")

    #  lectura del trimestre (filtrado por año seleccionado) 
    trimestres_disponibles = sorted(df.loc[df["ANO4"] == anio, "TRIMESTRE"].unique())
    trimestre = st.selectbox("Seleccione el trimestre:", trimestres_disponibles, key="trimestre_2")

    # filtro el dataframe por año y trimestre 
    filtrado = df[(df["ANO4"] == anio) & (df["TRIMESTRE"] == trimestre)]

    if filtrado.empty:
        st.warning("No hay datos disponibles para el año y trimestre seleccionados.")
        return

    #  agrupo edades en intervalos de 10 años 
    bins = range(0, 101, 10)  # Va en series de 0-9, 10-19, .. , 90-99
    labels = [f"{i}-{i+9}" for i in bins[:-1]]
    filtrado["grupo_edad"] = pd.cut(filtrado["CH06"], bins=bins, labels=labels, right=False)

    #  mapeo sexo a texto legible 
    filtrado["sexo"] = filtrado["CH04"].map({1: "Varón", 2: "Mujer"})

    #  agrupo por grupo de edad y sexo 
    conteo = (
        filtrado
        .groupby(["grupo_edad", "sexo"])["PONDERA"]
        .sum()
        .reset_index(name="Cantidad")
    )

    #  muestro gráfico de barras dobles 
    st.markdown("### 📊 Distribución poblacional por edad y sexo")
    plt.figure(figsize=(10, 6))
    sns.barplot(data=conteo, x="grupo_edad", y="Cantidad", hue="sexo")
    plt.title(f"Población por grupo de edad y sexo – {anio} T{trimestre}")
    plt.xlabel("Grupo de edad (años)")
    plt.ylabel("Cantidad de personas")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt.gcf())


# --------------------------------------------------------------------------------------
#Funcion para ejercicio 1.3.2



def edad_promedio_por_aglomerado(df):
    """
    Calcula y muestra la edad promedio por aglomerado
    para el último año y trimestre disponibles en el DataFrame.
    """

    # encabezado
    st.header("Edad promedio por aglomerado")
    st.markdown("Se permite visualizar la edad promedio de personas por aglomerado para el último semestre disponible con un formato a elección del usuario")

    # deteccion del ultimo trimestre y ultimo año
    ultimo_anio  = df["ANO4"].max()
    ultimo_trim  = df[df["ANO4"] == ultimo_anio]["TRIMESTRE"].max()
    st.info(f" Último período disponible: {ultimo_anio} - Trimestre {ultimo_trim}")

    # filtrado del DataFrame para ese año‑trimestre
    filtrado = df[(df["ANO4"] == ultimo_anio) & (df["TRIMESTRE"] == ultimo_trim)]
    if filtrado.empty:
        st.warning("No hay datos para el último período disponible.")
        return

    # calculo de la edad promedio por aglomerado

    edad_prom = (
        filtrado
        .groupby("AGLOMERADO")
        .apply(lambda g: (g["CH06"] * g["PONDERA"]).sum() / g["PONDERA"].sum())
        .reset_index()
        .rename(columns={0: "Edad promedio"})
    )

    # mapeo el código de aglomerado a su nombre legible
    edad_prom["Aglomerado"] = edad_prom["AGLOMERADO"].map(AGLOMERADO_STR)
    # Ordenar de mayor a menor edad promedio
    edad_prom = edad_prom.sort_values("Edad promedio", ascending=False)

    # 4)  visualización de tabla redondeada a 2 decimales
    st.markdown("### 📋 Edad promedio por aglomerado")

    st.markdown ("¿Cómo desea visualizar los datos?")

    # selector de grafico para el usuario
    vertical = st.toggle("Gráfico de barras vertical")
    horizontal = st.toggle("Gráfico de barras horizontal")
    tabla = st.toggle("Tabla")

    # grafico de barras VERTICAL
    if vertical:
        st.markdown("### 📊 Gráfico de barras (vertical)")

        # Ancho dinámico: 0.5 pulgadas por barra 
        ancho = max(14, len(edad_prom) * 0.5)
        fig, ax = plt.subplots(figsize=(ancho, 6))

        sns.barplot(
            data=edad_prom,
            x="Aglomerado", y="Edad promedio",
            palette="mako", ax=ax
        )

        # ajustes visuales
        ax.set_xlabel("Aglomerado", fontsize=11)
        ax.set_ylabel("Edad promedio", fontsize=11)
        ax.set_xticklabels(ax.get_xticklabels(),
        rotation=70, ha='right', fontsize=9)  # evita solapamiento
        ax.tick_params(axis='y', labelsize=10)

        plt.tight_layout()
        st.pyplot(fig)

    # grafico de barras HORIZONTAL

    if horizontal:
        st.markdown("### 📊 Gráfico de barras (horizontal)")

        # Alto dinámico: 0.6 pulgadas por barra (mínimo 6)
        alto = max(6, len(edad_prom) * 0.6)
        fig, ax = plt.subplots(figsize=(12, alto))

        sns.barplot(
            data=edad_prom,
            y="Aglomerado", x="Edad promedio",
            palette="mako", ax=ax
        )

        # Ajustes estéticos
        ax.set_xlabel("Edad promedio", fontsize=12)
        ax.set_ylabel("")
        ax.tick_params(axis='y', labelsize=10)
        ax.tick_params(axis='x', labelsize=11)

        plt.tight_layout()
        st.pyplot(fig)
    
    if tabla:
        tabla = edad_prom[["Aglomerado", "Edad promedio"]].copy()
        tabla["Edad promedio"] = tabla["Edad promedio"].round(2)
        st.dataframe(tabla, use_container_width=True, hide_index=True)

#----------------------------------------------------------------------------------------
#Funcion para ejercicio 1.3.3

def evolucion_dependencia_demografica(df):
    """
    Muestra la evolución de la dependencia demográfica para un aglomerado seleccionado.
    """
    st.header("Evolución de la dependencia demográfica")
    st.markdown("Se representa la evolución de la dependencia demográfica en los semestres disponibles del aglomerado seleccionado")

    # mapeo aglomerados por nombre
    df["Aglomerado_nombre"] = df["AGLOMERADO"].map(AGLOMERADO_STR)

    aglomerado_seleccionado = st.selectbox("Seleccione un aglomerado:", df["Aglomerado_nombre"].dropna().unique(), key="select_aglo_dep")

    #  filtrado de aglomerado 
    aglo_cod = {v: k for k, v in AGLOMERADO_STR.items()}[aglomerado_seleccionado]
    df_aglo = df[df["AGLOMERADO"] == aglo_cod].copy()

    #evaluo posible error por falta de dfatos
    if df_aglo.empty:
        st.warning("No hay datos para este aglomerado.")
        return

    #  clasificacion por edades (EDAD en columna--> CHO6)
    df_aglo["grupo_etario"] = pd.cut(
        df_aglo["CH06"],
        bins=[0, 14, 64, float('inf')],
        labels=["0-14", "15-64", "65+"],
        right=True
    )

    # Agrupar por año-trimestre
    evolucion = (
        df_aglo
        .groupby(["ANO4", "TRIMESTRE", "grupo_etario"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    
    
    # Calcular dependencia
    poblacion_dependiente=evolucion["0-14"] + evolucion["65+"]
    
    evolucion["Dependencia (%)"] = (poblacion_dependiente / evolucion["15-64"]) * 100
    evolucion["Periodo"] = evolucion["ANO4"].astype(str) + " - T" + evolucion["TRIMESTRE"].astype(str)

    # mostrar tabla con la evolucion de la dependencia 
    st.markdown("### 📋 Tabla de evolución")
    st.dataframe(evolucion[["Periodo", "Dependencia (%)"]], use_container_width=True)

    # visualización de grafico. se utiliza grafico de lineas 
    st.markdown("### 📈 Evolución temporal de la dependencia demográfica")
    fig, ax = plt.subplots(figsize=(12, 4))
    sns.lineplot(data=evolucion, x="Periodo", y="Dependencia (%)", marker="o", ax=ax)
    ax.set_title(f"Dependencia demográfica en {aglomerado_seleccionado}")
    ax.set_ylabel("Dependencia (%)")
    ax.set_xlabel("Período")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)



# --------------------------------------------------------------------------------------
#Funcion para ejercicio 1.3.4


def media_mediana_edad(df):
    """
    Permite seleccionar año y trimestre y muestra
    la media y mediana de la edad de la población.
    """

    st.header("Media y mediana de la edad de la población")
    st.markdown("Se informa la media y mediana de la edad de la población por cada año y trimestre")

    # usuario selecciona año y trimestre
    anios = sorted(df["ANO4"].unique())
    anio = st.selectbox("Seleccione el año:", anios, index=len(anios)-1, key="anio_1")

    trimestres = sorted(df.loc[df["ANO4"] == anio, "TRIMESTRE"].unique())
    trimestre = st.selectbox("Seleccione el trimestre:", trimestres, key="trimestre_1")

    # filtro dataframe
    subset = df[(df["ANO4"] == anio) & (df["TRIMESTRE"] == trimestre)]

    if subset.empty:
        st.warning("No hay datos para el período seleccionado.")
        return

    # calculo media y mediana
    media   = subset["CH06"].mean()
    mediana = subset["CH06"].median()

    #  visualizacion de resultados
    col1, col2 = st.columns(2)
    col1.metric("Edad media",   f"{media:,.2f} años")
    col2.metric("Edad mediana", f"{mediana:,.2f} años")
