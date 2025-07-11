import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from constants import AGLOMERADO_STR


def tipo_viviendas(df):
    st.subheader("1.4.2: proporción de viviendas según su tipo:")
    labels = {
        1: "casa",
        2: "departamento",
        3: "pieza de inquilinato",
        4: "pieza en hotel/pensión",
        5: "local no construido para habitación",
        6: "otros"
    }
    # Agrupar por tipo de vivienda y sumar los pesos
    sizes = df.groupby("IV1")["PONDERA"].sum()
    # si una etiqueta tiene 0 no aparece en la pie chart
    etiquetas = [labels[i] for i in sizes.index]
    # necesito toda la cantidad para crear el porcentaje
    totales = sizes.sum()

    etiquetas_con_porcentaje = [
        f"{label} ({round(sizes[i]/totales*100, 1)}%)"
        for i, label in zip(sizes.index, etiquetas)
    ]

    fig1, ax1 = plt.subplots(figsize=(5, 5))

    wedges, texts, autotexts = ax1.pie(
        sizes,
        labels=None,
        startangle=90,
        autopct=''
    )

    ax1.legend(wedges, etiquetas_con_porcentaje, loc="upper center",
               bbox_to_anchor=(0.5, 1.15), ncol=2, frameon=False)

    ax1.axis('equal')

    st.pyplot(fig1)


def tipo_piso_viviendas(df):
    st.subheader("1.4.3: Material predominante en los pisos por aglomerado:")

    # tipos de piso
    pisosInteriores = {
        1: "mosaico/baldosa/madera/cerámica/alfombra",
        2: "cemento/ladrillo fijo",
        3: "ladrillo suelto/tierra",
        4: "otros"
    }

    suma = df.groupby(["AGLOMERADO", "IV3"])["PONDERA"].sum().reset_index()

    max = suma.groupby("AGLOMERADO")["PONDERA"].idxmax()

    filtrado = suma.loc[max]
    filtrado.columns = ["Aglomerado", "CódigoMaterial", "SumaPondera"]

    filtrado["Material predominante"] = filtrado["CódigoMaterial"].map(
        pisosInteriores)
    filtrado["Aglomerado"] = filtrado["Aglomerado"].map(AGLOMERADO_STR)

    st.dataframe(filtrado[["Aglomerado", "Material predominante"]])

    """ 
        Primero sumo las ponderaciones agrupando por aglomerado y codigo de material asi despues
        puedo sacar el maximo de cada uno(max), con idxmax() busco que material de piso tiene 
        la mayor suma.

        Se mapea por cada codigo de material y le coloca el nombre al igual que con cada aglomerados
        por ultimo muestra el df filtrando por aglomerado y piso.
    """


def porcentaje_banio_aglomerados(df):
    st.subheader("1.4.4: Proporción de viviendas con baño dentro del hogar por aglomerado:")

    conBanio = df[df["IV8"] == 1].groupby("AGLOMERADO")["PONDERA"].sum()
    totalViviendas = df.groupby("AGLOMERADO")["PONDERA"].sum()
    porcentaje = (conBanio / totalViviendas * 100).round(2)

    resultado = pd.DataFrame({
        "Aglomerado": porcentaje.index.map(AGLOMERADO_STR),
        "Porcentaje": porcentaje.values
    })

    st.bar_chart(resultado.set_index("Aglomerado"))

    """ 
    conBanio --> cantidad ponderada de los aglomerados que tienen baño
    totalViviendas --> cantidad total de viviendas por aglomerado
    entonces calculo el porcentaje y cortando con dos decimales

    Se crea el DataFrame con "Aglomerado" que mapea por cada nombre y su porcentaje y uso un 
    bar chart con esos datos.
    
    """

def evolucion_tenencia_por_aglomerado(df):
    tenencia = {
        1: "Propietario de la vivienda y el terreno",
        2: "Propietario de la vivienda solamente",
        3: "Inquilino/arrendatario de la vivienda",  
        4: "Ocupante por pago de impuestos/expensas",
        5: "Ocupante en relación de dependencia",
        6: "Ocupante gratuito (con permiso)",
        7: "Ocupante de hecho (sin permiso)",
        8: "Está en sucesión",
        9: "Otros"
    }
    nombresAglomerados = sorted(AGLOMERADO_STR.values())


    st.subheader("Seleccioná un Aglomerado")
    nombre = st.select_slider("",options=nombresAglomerados,)

    for cod, nom in AGLOMERADO_STR.items(): 
        if nom == nombre:
            codAglomerados = cod
            break  


    nombresTenencia = list(tenencia.values())

    tenencias_seleccionadas = st.multiselect(
        "Elegí los tipos de tenencia",
        options=nombresTenencia
    )
    st.subheader("1.4.5: evolución del régimen de tenencia por Trimestre:")
    codigos = [codigo for codigo, nombre in tenencia.items() if nombre in tenencias_seleccionadas]

    dfFiltrado = df[df["AGLOMERADO"] == codAglomerados]

    dfAgrupado = dfFiltrado.groupby(["TRIMESTRE", "II7"])["PONDERA"].sum().reset_index()
    cantTotal = dfAgrupado.groupby("TRIMESTRE")["PONDERA"].transform("sum")
    dfAgrupado["Porcentaje"] = (dfAgrupado["PONDERA"] / cantTotal * 100).round(2)
    dfAgrupado = dfAgrupado[dfAgrupado["II7"].isin(codigos)]
    
    dfAgrupado["Tenencia"] = dfAgrupado["II7"].map(tenencia)


    t1 = dfAgrupado[dfAgrupado["TRIMESTRE"] == 1][["Tenencia", "Porcentaje"]].rename(columns={"Porcentaje": "Trimestre 1"})
    t2 = dfAgrupado[dfAgrupado["TRIMESTRE"] == 2][["Tenencia", "Porcentaje"]].rename(columns={"Porcentaje": "Trimestre 2"})
    t3 = dfAgrupado[dfAgrupado["TRIMESTRE"] == 3][["Tenencia", "Porcentaje"]].rename(columns={"Porcentaje": "Trimestre 3"})
    t4 = dfAgrupado[dfAgrupado["TRIMESTRE"] == 4][["Tenencia", "Porcentaje"]].rename(columns={"Porcentaje": "Trimestre 4"})


    tabla = t1.merge(t2, on="Tenencia", how="outer").merge(t3, on="Tenencia", how="outer").merge(t4, on="Tenencia", how="outer").round(2)

    if not dfAgrupado.empty:
        st.dataframe(tabla.reset_index(drop=True))
    else:
        st.warning("Elegí al menos un tipo de tenencia.")

""" 
    creo una lista de las tenencias así el usuario puede seleccionar
    agarro los codigos de las tenencias seleccionadas
    filtro el df por el aglomerado elegido por el usuario
    agrupo por trimestre y tenencia y sumo la pondera
    con transform() lo que hago es sumar el total del la pondera de cada trimestre para luego 
    calcular el porcentaje de cada uno
    por ultimo filtro solo las tenencias que seleccionó el user
    
    para terminar creo 4 df y los uno por los 4 trimestres(aunque no se usen todos) 
    
"""

def viviendas_villa_emerg_aglomerado(df):
    st.subheader("1.4.6: Viviendas en villa de emergencia por aglomerado:")

    enVilla = df[df["IV12_3"] == 1].groupby("AGLOMERADO")["PONDERA"].sum()

    total = enVilla.sum()
    porcentaje = (enVilla / total * 100).round(2)

    tabla = pd.DataFrame({
        "Aglomerado": enVilla.index.map(AGLOMERADO_STR),
        "Viviendas en villa": enVilla,
        "Porcentaje nacional": porcentaje
    }).sort_values("Viviendas en villa", ascending=False).reset_index(drop=True)

    st.dataframe(tabla)

    """ 
        agrupo aglomerado y pondera, filtro por vivienda en villa de emergencia
        saco un total de la cantidad de casas en villa de emergencia para el porcentaje
        por ultimo creo el DF donde muestra cada Aglomerado con la cantidad de Viviendas en villa y el porcentaje
        (decrecientemente)
        para comprobar se puede sumar todos los porcentajes y te da 100

    """
    
def viviendas_cond_habitabilidad_aglomerado(df):
    st.subheader("1.4.7: Porcentaje de viviendas por Condición de Habitabilidad: ")

    agrupado = df.groupby(["AGLOMERADO", "CONDICION_DE_HABITABILIDAD"])["PONDERA"].sum().reset_index()

    totales = agrupado.groupby("AGLOMERADO")["PONDERA"].transform("sum")
    agrupado["Porcentaje"] = (agrupado["PONDERA"] / totales * 100).round(2)

    agrupado["Aglomerado"] = agrupado["AGLOMERADO"].map(AGLOMERADO_STR)

    condBuena = agrupado[agrupado["CONDICION_DE_HABITABILIDAD"] == "buena"][["Aglomerado", "Porcentaje"]].rename(columns={"Porcentaje": "Buena"})
    condRegular = agrupado[agrupado["CONDICION_DE_HABITABILIDAD"] == "regular"][["Aglomerado", "Porcentaje"]].rename(columns={"Porcentaje": "Regular"})
    condInsuficiente = agrupado[agrupado["CONDICION_DE_HABITABILIDAD"] == "insuficiente"][["Aglomerado", "Porcentaje"]].rename(columns={"Porcentaje": "Insuficiente"})
    condSaludables = agrupado[agrupado["CONDICION_DE_HABITABILIDAD"] == "saludables"][["Aglomerado", "Porcentaje"]].rename(columns={"Porcentaje": "Saludables"})

    tabla = condBuena.merge(condRegular, on="Aglomerado", how="outer").merge(condInsuficiente, on="Aglomerado", how="outer").merge(condSaludables, on="Aglomerado", how="outer").round(2)


    st.dataframe(tabla)
    # boton para descargar csv
    csv = tabla.to_csv(index=False, sep=";").encode("utf-8")
    st.download_button(
        label="⬇️Descargar CSV",
        data=csv,
        file_name="porcentaje_viviendas_por_condicion.csv",
        mime="text/csv"
    )

""" 
    agrupo aglomerado y condicion de habitabilidad, sumo la pondera
    Separamos cada condición en un DataFrame y mergeamos todos
    totales tiene el total de viviendas ponderadas para calcular el porcentaje
    
    reemplazo el codigo de cada aglomerado con el nombre
    condBuena, condRegular, condInsuficiente,condSaludables son DataFrames donde cada una tiene aglomerado y el
    tipo de condicion de habitabilidad
    
    por ultimo hago un merge de las 4 asi tengo un solo DataFrame pero con las cuatro condiciones 
    usando how="outer" para no perder datos, ya que aunque sea NaN aparece igual 
"""