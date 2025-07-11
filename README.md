# Encuest.Ar 🇦🇷

## Descripción 📝
Encuest.Ar es una aplicación que procesa y analiza información específica extraída de los microdatos de La Encuesta Permanente de Hogares (EPH) que lleva a cabo el Instituto Nacional de Estadística y Censos (INDEC) de Argentina.

El objetivo del proyecto es transformar datos crudos en información comprensible para que cualquier usuario pueda analizar tendencias y características socioeconómicas de la población argentina.

## Estructura del Proyecto 📁
- **files/individuos/**: Contiene los archivos de datos de la EPH por trimestre referente a los individuos
- **files/hogares/** : Contiene los archivos de datos de el EPH por trimestre referente a los hogares
- **notebook/**: Jupyter notebooks para análisis de datos y generación de estadísticas
- **src/**: Código fuente principal de la aplicación
- **src/streamlit/pages**: Contiene las paginas de la app de streamlit
- **src/utils_*.py** : Funciones especificadas por tematica


## Requisitos Previos ⚙️
- Python 3.12.9
- pip (gestor de paquetes de Python)
- Conexión a Internet para instalar dependencias

## Instalación 🔧

1. **Clonar el repositorio**
   ```bash
   git clone <URL_del_repositorio>
   cd Encuest.Ar
   ```

2. **Crear un entorno virtual (recomendado)**
   ```bash
   python -m venv venv
   ```

3. **Activar el entorno virtual**
   - En Windows:
   ```bash
   venv\Scripts\activate
   ```
   - En macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

## Uso 🚀

## 📥 Ingreso de Datos
Colocá los archivos .txt originales de la EPH en las carpetas:
   - files/hogares/
   - files/individuos/
⚠️ Asegurate de que el formato de nombre sea el oficial (por ejemplo: usu_hogar_T120.txt).

## 🧪 Procesamiento de Datos (Notebooks)

### ⚠️ IMPORTANTE: Secuencia de ejecución de notebooks ⚠️
Los notebooks deben ejecutarse en un orden específico para el correcto funcionamiento del proyecto:

1. **Primero**: `generar_dataset.ipynb` - Crea los datasets base unificados
2. **Segundo**: `hogares.ipynb` - Procesa y agrega columnas relacionadas con los hogares
3. **Tercero**: `individuos.ipynb` - Procesa y agrega columnas relacionadas con los individuos
4. **Cuarto**: `outputs.ipynb` - Genera los análisis y visualizaciones finales

No seguir este orden puede resultar en errores o resultados incorrectos, ya que cada notebook depende de las transformaciones realizadas en el anterior.

### Análisis mediante Notebooks 📊
El proyecto incluye varios notebooks para realizar análisis específicos:
- `notebook/hogares.ipynb`: Análisis de datos a nivel hogar
- `notebook/individuos.ipynb`: Análisis de datos a nivel individual
- `notebook/outputs.ipynb`: Generación de resultados y estadísticas

Para ejecutarlos:
```bash
jupyter notebook notebook/
```

### Interfaz Gráfica con Streamlit 💻
Puede visualizar el programa mediante la interfaz gráfica ejecutando:

```bash
streamlit run src/streamlit/Inicio.py
```

La aplicación se abrirá en su navegador predeterminado, mostrando un menu con las siguientes paginas:
- Inicio: Contiene información general sobre la tematica de la pagina
- Carga de datos : Su objetivo principal es verificar la consistencia entre los archivos proporcionados y permitir la actualizacion de los archivos unificados.
- Caracteristicas demoraficas : Contiene información relacionada a la características demográficas de la población argentina según la EPH.
- Caracteristicas de la vivienda : Contiene información relacionada a las características de las viviendas de la población argentina según la EPH.
- Actividad y empleo : Contiene información relacionada a la actividad y empleo según la
EPH.
- Educacion : Contiene información relacionada al nivel de educación alcanzado por la población argentina según la EPH.
- Ingresos : Calcula el porcentaje de hogares de 4 integrantes que están por debajo de la línea de pobreza e indigencia, según los ingresos (ITF) y la canasta básica del trimestre seleccionado por el usuario.

## Consideraciones Importantes ⚠️

1. **Formato de los archivos de entrada**: Los archivos de la EPH deben mantener el formato original del INDEC para ser procesados correctamente.

2. **Consumo de recursos**: El procesamiento de grandes volúmenes de datos puede requerir considerable memoria RAM, especialmente al unificar múltiples trimestres.

3. **Versiones de dependencias**: El proyecto ha sido probado con las versiones específicas indicadas en requirements.txt. Usar otras versiones podría ocasionar incompatibilidades.

4. **Almacenamiento**: Asegúrese de tener suficiente espacio en disco para almacenar los archivos generados durante el procesamiento.

---
