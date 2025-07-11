import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

from constants import AGLOMERADO_STR  

def edad_promedio_por_aglomerado(df):
    """
    Calcula y muestra la edad promedio por aglomerado
    para el último año y trimestre disponibles en el DataFrame.
    """

    # encabezado
    st.header("Edad promedio por aglomerado")

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

        # Ancho dinámico: 0.5 pulgadas por barra (mínimo 14)
        ancho = max(14, len(edad_prom) * 0.5)
        fig, ax = plt.subplots(figsize=(ancho, 6))

        sns.barplot(
            data=edad_prom,
            x="Aglomerado", y="Edad promedio",
            palette="mako", ax=ax
        )

        # Ajustes estéticos
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
