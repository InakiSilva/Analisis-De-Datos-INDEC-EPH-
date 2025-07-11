import os
from constants import INDIVIDUAL_DATA_OUT_PATH, HOGAR_DATA_OUT_PATH, DATA_OUT_PATH, FILES_HOGARES_DIRECTORY, FILES_INDIVIDUOS_DIRECTORY

def unir_archivos(path_carpeta_archivos, path_archivo_out):
    encabezado = True
    with path_archivo_out.open("w") as archivo_salida:
        for archivo in path_carpeta_archivos.iterdir():
            try:
                with archivo.open('r') as a:
                    for i, line in enumerate(a):
                        if i == 0 and not encabezado:
                            continue
                        archivo_salida.write(line.rstrip('\n') + '\n')
                encabezado = False
            except:
                continue


def unir_files():
    def is_not_empty(folder):
        return any(folder.iterdir())
    
    #Creo la carpeta data_out
    if not os.path.exists(DATA_OUT_PATH):
        os.makedirs(DATA_OUT_PATH)

    if is_not_empty(FILES_HOGARES_DIRECTORY) and is_not_empty(FILES_INDIVIDUOS_DIRECTORY):
        unir_archivos(FILES_HOGARES_DIRECTORY,  HOGAR_DATA_OUT_PATH)
        unir_archivos(FILES_INDIVIDUOS_DIRECTORY, INDIVIDUAL_DATA_OUT_PATH)
        return True
    return False

if __name__ == "__main__":
    unir_files()

