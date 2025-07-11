
import csv

def extraer (path, columnas_deseadas):
    '''
        Extrae las columnnas del archivo que se especifican como parametro 

        parametros:
            path : path del archivo a extraer los datos
            columnas_deseadas : una lista donde sus elementos son nombres de los encabezados interesados
        
        return :
            Devuelve una lista de diccionarios, con los datos de las columnas deseadas
    '''
    with open(path, 'r', encoding='utf-8') as file:
        lector = csv.DictReader(file, delimiter=';')

        # Usamos map para transformar cada fila en solo las columnas deseadas
        datos_seleccionados = list(map(lambda fila: {col: fila[col] for col in columnas_deseadas}, lector))

    return datos_seleccionados


    
def escribir (path, nuevas_fila):
    '''
        Escribe en el archivo especificado, las nuevas columnas

        parametros:
            path : path del archivo a escribir las nuevas columnas
            nuevas_fila : lista de diccionario que representan las nuevas filas a escribir

    '''
    # Leer archivo original
    with open(path, encoding='utf-8') as file:
        lector = csv.DictReader(file, delimiter=';')
        lista = list(lector)

    # Agregar nuevas columnas por fila
    for i, linea in enumerate(lista):
        linea.update(nuevas_fila[i])

    # Obtener todos los encabezados (columnas) actualizados
    fieldnames = list(lista[0].keys())

    # Escribir archivo actualizado
    with open(path, mode='w', encoding='utf-8', newline='') as archivo_salida:
        writer = csv.DictWriter(
            archivo_salida, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(lista)