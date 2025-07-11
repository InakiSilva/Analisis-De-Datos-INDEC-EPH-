import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def nivel_ed_anios(df, anio):
    """
    Genera y muestra un gráfico de barras con la cantidad de personas por nivel educativo alcanzado
    para un año específico. Utiliza los datos del DataFrame filtrando por el año dado,
    agrupa por el campo 'NIVEL_ED_str' y suma la ponderación de cada grupo. El resultado se visualiza
    en una gráfica y se muestra en la página de educación.
    """
    df_anio = df[df['ANO4'] == anio]
    conteo_nivel = df_anio.groupby('NIVEL_ED_str')['PONDERA'].sum().sort_values(ascending=False)
    st.header(f'📊Cantidad de personas por nivel educativo en {anio}')
    
    # Gráfico con Matplotlib
    fig, ax = plt.subplots()
    conteo_nivel.plot(kind='bar', ax=ax)
    # Rota etiquetas y alinea a la derecha
    plt.xticks(rotation=45, ha='right')  
    plt.xlabel('Nivel educativo')
    plt.ylabel('Cantidad de personas')
    plt.tight_layout()

    # Agregar valores arriba de cada barra
    for i, v in enumerate(conteo_nivel):
        ax.text(i, v + max(conteo_nivel)*0.01, f'{int(v):,}', ha='center', va='bottom', fontsize=9, rotation=0)
    
    st.pyplot(fig)



def nivel_educativo_por_grupo_etario(df):
    """
    Muestra el nivel educacional más común para diferentes grupos etarios:
    - 20-30 años
    - 30-40 años
    - 40-50 años
    - 50-60 años
    - Mayores de 60 años
    
    Permite al usuario elegir qué rangos de edad visualizar: uno solo, 
    un conjunto de ellos o todos a la vez.
    Se muestra la información utilizando un gráfico de barras horizontal en Matplotlib.
    """
    st.header("👥 Nivel educativo por grupo etario")
    
    # Definir los rangos de edad
    grupos_etarios = [
        ('20-30 años', 20, 30),
        ('30-40 años', 30, 40),
        ('40-50 años', 40, 50),
        ('50-60 años', 50, 60),
        ('Mayores de 60 años', 60, 200)  
    ]
    
    # Crear un selector multiselección para los grupos etarios
    nombres_grupos = [grupo[0] for grupo in grupos_etarios]
    grupos_seleccionados = st.multiselect(
        '¿Qué grupos etarios deseas visualizar?',
        options=nombres_grupos,
        default=[],  # Sin valores predeterminados
        help="Selecciona uno o varios grupos de edad para visualizar su información educativa"
    )
    
    # Si no se selecciona ninguno, mostrar mensaje y salir
    if not grupos_seleccionados:
        st.warning("Por favor, selecciona al menos un grupo etario para visualizar.")
        return
    
    # Recopilar datos para todos los grupos seleccionados
    datos_grupos = {}
    niveles_educativos = set()  # Para almacenar todos los niveles educativos encontrados
    
    for nombre_grupo in grupos_seleccionados:
        idx = nombres_grupos.index(nombre_grupo)
        nombre_grupo, edad_min, edad_max = grupos_etarios[idx]
        
        # Filtrar por rango de edad
        df_grupo = df[(df['CH06'] >= edad_min) & (df['CH06'] < edad_max)]
        
        if not df_grupo.empty:
            # Agrupar por nivel educativo y contar
            nivel_edu_counts = df_grupo.groupby('NIVEL_ED_str')['PONDERA'].sum()
            
            # Calcular porcentajes
            total = nivel_edu_counts.sum()
            porcentajes = (nivel_edu_counts / total * 100).round(1)
            
            # Guardar datos para este grupo
            datos_grupos[nombre_grupo] = porcentajes
            
            # Agregar los niveles educativos encontrados al conjunto
            niveles_educativos.update(porcentajes.index)
        else:
            st.warning(f"No hay datos para el grupo etario: {nombre_grupo}")
    
    # Si tenemos datos, crear el gráfico
    if datos_grupos:
        # Convertir el conjunto de niveles educativos a una lista ordenada
        niveles_list = sorted(list(niveles_educativos))
        
        # Crear una matriz de datos para el gráfico
        # Cada fila es un grupo etario, cada columna es un nivel educativo
        data = []
        labels = []
        
        for nombre_grupo, porcentajes in datos_grupos.items():
            row = []
            labels.append(nombre_grupo)
            for nivel in niveles_list:
                if nivel in porcentajes:
                    row.append(porcentajes[nivel])
                else:
                    row.append(0)  # Si no hay datos para este nivel en este grupo
            data.append(row)
        
        # Crear el gráfico horizontal
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Colores vibrantes para las barras
        colors = plt.cm.viridis(np.linspace(0, 1, len(niveles_list)))
        
        # Posiciones de las barras
        pos = np.arange(len(labels))
        bar_height = 0.8 / len(niveles_list)
        
        # Crear las barras para cada nivel educativo
        bars = []
        for i, nivel in enumerate(niveles_list):
            values = [row[i] for row in data]
            bars.append(ax.barh(
                pos + i * bar_height - 0.4 + bar_height/2,
                values,
                height=bar_height,
                color=colors[i],
                label=nivel
            ))
        
        # Configurar el gráfico
        ax.set_yticks(pos)
        ax.set_yticklabels(labels)
        ax.set_xlabel('Porcentaje (%)')
        ax.set_title('Nivel educativo por grupo etario')
        
        # Añadir una leyenda
        ax.legend(title="Nivel educativo", bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Añadir porcentajes en las barras
        for i, nivel in enumerate(niveles_list):
            for j, v in enumerate(bars[i]):
                width = v.get_width()
                if width > 1:  # Solo mostrar etiqueta si el porcentaje es mayor a 1%
                    ax.text(
                        width + 0.5, 
                        v.get_y() + v.get_height()/2,
                        f"{width:.1f}%",
                        va='center',
                        fontsize=8
                    )
        
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.warning("No hay datos disponibles para los grupos seleccionados.")



def boton_descarga(ranking):
    """
    Crea un botón de descarga para el archivo de ranking de aglomerados.
    Permite a los usuarios descargar el archivo CSV con los datos del ranking.
    """
    st.header('📈Ranking de aglomerados')
    
    st.write(
        'Descargue el Ranking de los 5 aglomerados con mayor porcentaje de hogares '
        'con dos o más ocupantes con estudios universitarios o superiores '
        'finalizados en formato CSV:'
    )
    
    # Mostrar el botón de descarga
    csv = ranking.to_csv().encode("utf-8")
    
    st.download_button(
        label="⬇️Descargar CSV",
        data=csv,
        file_name="ranking_aglomerados.csv",
        mime="text/csv"
    )

def alfabetizacion_todos_los_anios(df):
    """
    Muestra, año tras año, el porcentaje de personas mayores a 6 años capaces e incapaces de leer y escribir.
    Utiliza métricas de Streamlit para una visualización clara y directa.
    """
    anios = sorted(df['ANO4'].unique())
    for anio in anios:
        st.subheader(f"📚 Alfabetización en {anio}")
        
        df_anio = df[(df['ANO4'] == anio) & (df['CH06'] > 6)]
        total = df_anio['PONDERA'].sum()
        
        if total > 0:
            capaces = df_anio[df_anio['CH09'] == 1]['PONDERA'].sum()
            incapaces = df_anio[df_anio['CH09'] == 2]['PONDERA'].sum()
            
            # Calcular porcentajes
            porcentaje_capaces = capaces / total * 100
            porcentaje_incapaces = incapaces / total * 100
            
            # Crear dos columnas para las métricas
            col1, col2 = st.columns(2)
            
            # Mostrar métricas en las columnas
            with col1:
                st.metric(
                    label="Capaces de leer y escribir",
                    value=f"{porcentaje_capaces:.1f}%",
                )
            
            with col2:
                st.metric(
                    label="Incapaces de leer y escribir",
                    value=f"{porcentaje_incapaces:.1f}%",
                )
        else:
            st.warning(f"No hay datos disponibles para el año {anio}")
        
        st.divider()

