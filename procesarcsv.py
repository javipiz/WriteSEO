"""
@file procesarcsv.py
@brief En este archivo se implementan todas las funciones para manejar los archivos de entrada de keywords, sobre todo, si se hace mediante un archivo.csv
"""
import csv
import os
from difflib import SequenceMatcher


def leer_keywords_existentes(nombre_archivo):
    """
    @brief Lee las keywords existentes desde un archivo CSV. La función lee las keywords existentes desde la segunda columna de un archivo CSV y las devuelve como una lista.
    @param nombre_archivo Ruta del archivo CSV que contiene las keywords.
    @return Lista de keywords existentes.
    """
    if not os.path.isfile(nombre_archivo):
        return []
    with open(nombre_archivo, "r", newline="", encoding="utf-8") as archivo_csv:
        lector = csv.reader(archivo_csv)
        next(lector, None)  # Saltar el encabezado
        keywords_list = [fila[1] for fila in lector if len(fila) > 1]  # Asegurarse de que la fila tenga al menos dos columnas
        return keywords_list


def son_similares(a, b, umbral=0.8):
    """
    @brief Compara la similitud entre dos palabras. Utiliza la clase SequenceMatcher para calcular la ratio de similitud entre dos palabras y devuelve True si la ratio es mayor que el umbral especificado, False en caso contrario.
    @param a Primera palabra a comparar.
    @param b Segunda palabra a comparar.
    @param umbral Umbral de similitud (opcional, por defecto 0.8).
    @return True si las palabras son similares, False en caso contrario.
    """
    return SequenceMatcher(None, a, b).ratio() > umbral



def eliminar_similares(keywords, umbral=0.8):
    """
    @brief Elimina palabras clave que son similares entre sí.Itera sobre una lista de palabras clave y elimina aquellas que son similares entre sí, según un umbral de similitud especificado.
    @param keywords Lista de palabras clave a procesar.
    @param umbral Umbral de similitud (opcional, por defecto 0.8).
    @return Lista de palabras clave únicas, sin duplicados similares.
    """
    keywords_unicas = []
    while keywords:
        palabra = keywords.pop(0)
        keywords_unicas.append(palabra)
        keywords = [k for k in keywords if not son_similares(palabra, k, umbral)]
    return keywords_unicas


def escribir_keywords_en_txt(keywords, nombre_txt):
    """
    @brief Escribe una lista de keywords en un archivo de texto. La función escribe una lista de keywords en un archivo de texto, ordenando las keywords alfabéticamente para facilitar la lectura.
    @param keywords Lista de palabras clave a escribir en el archivo de texto.
    @param nombre_txt Ruta del archivo de texto donde se escribirán las keywords.
    @return None
    """
    with open(nombre_txt, "w", encoding="utf-8") as archivo_txt:
        for keyword in sorted(keywords):  # Ordenar las keywords para facilitar la lectura
            archivo_txt.write(keyword + '\n')



def procesar_archivo_csv(nombre_csv, nombre_txt):
    """
    @brief Procesa un archivo CSV y escribe las keywords únicas en un archivo de texto. La función verifica si un archivo CSV existe, lee las keywords, elimina las similares y las escribe en un archivo de texto.
    @param nombre_csv Ruta del archivo CSV que contiene las keywords.
    @param nombre_txt Ruta del archivo de texto donde se escribirán las keywords únicas.
    @return None
    """
    if not os.path.isfile(nombre_csv):
        #No has introducido un .csv con palabras clave. (opcional)
        return

    keywords = leer_keywords_existentes(nombre_csv)
    keywords_unicas = eliminar_similares(keywords)
    escribir_keywords_en_txt(keywords_unicas, nombre_txt)
    print(f"Palabras clave únicas del archivo {nombre_csv} han sido escritas en {nombre_txt}")


if __name__ == '__main__':
    procesar_archivo_csv('CSV/palabrasclave.csv', '2. Keywords.txt')
