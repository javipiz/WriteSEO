"""
@file writeSEO.py
@brief Este archivo contiene las funciones principales para la generación de contenido con IA 
"""
import csv #manejo de archivos .csv
from openai import OpenAI
import re # Facilita la creación de expresiones regulares
import concurrent.futures
import threading
import requests
import os
from newspaper import Article 
import tiktoken #Calcular los tokens de un texto según OpenIA
from youtubesearchpython import VideosSearch #Busquedas vídeos
import unidecode
from PIL import Image # Manejo de datos de Imagenes
from io import BytesIO # Manejo de Imágenes
import previsualizaHTML
import procesarcsv


openai = OpenAI(api_key="temp")

# Leer las API keys de archivos de texto. Al menos debe de haber una API. Las introduce en una lista

with open("0. ValueSERP.txt", "r", encoding="utf-8") as file:
    apis_valueserp = [line.strip() for line in file]
    
with open("1. OpenAI.txt", "r", encoding="utf-8") as file:
    apis_openai = [line.strip() for line in file]


#En el caso de que se haya incluido un .csv con palabras clave (ver documentación) carga esas palabras clave en el archivo 2. Keywords y elimina las duplicadas y las muy similares.

procesarcsv.procesar_archivo_csv('CSV/palabrasclave.csv', '2. Keywords.txt')

# Leer el número de palabras clave existentes en el archivo Keywords.txt. Las introduce en una lista
with open("2. Keywords.txt", "r", encoding="utf-8") as file:
    keywords = [line.strip() for line in file]

# Función para cargar el contenido de un archivo

def load_component(file_path):
    """
    @brief Carga el contenido de un archivo.
    @param ruta_archivo La ruta del archivo a cargar.
    @return El contenido del archivo.
    @note Esta función lee el contenido de un archivo y lo devuelve como una cadena.Se asume que el archivo está codificado en UTF-8.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().strip()

# Función para calcular el número de tokens de un prompt


def calcular_numero_tokens(texto, modelo="gpt-3.5-turbo-16k"):
    """
    @brief Calcula el número de tokens en un texto según un modelo de lenguaje 
    @param[in] texto Texto a analizar 
    @param[in] modelo Modelo de lenguaje a utilizar (por defecto "gpt-3.5-turbo-16k") @return Número de tokens encontrados en el texto. 
    """
    encoding = tiktoken.encoding_for_model(modelo)
    tokens = encoding.encode(texto)
    return len(tokens)

# Función para calcular el coste de una petición a la IA de OpenAI

def calcular_coste(tokens_usados, precio_por_1000_tokens=0.003):
    """
    @brief Calcula el coste de un texto según el número de tokens utilizados 
    @param[in] tokens_usados Número de tokens utilizados en el texto 
    @param[in] precio_por_1000_tokens Precio por 1000 tokens (por defecto 0.003) 
    @return Coste del texto según el número de tokens utilizados 
    """
    return (tokens_usados / 1000) * precio_por_1000_tokens

# Función para calcular el coste de un texto devuelto por la IA de OpenAI

def calcular_coste_generado(tokens_usados, precio_por_1000_tokens=0.004):
    """
    @brief Calcula el coste de un texto devuelto por la IA según el número de tokens utilizados 
    @param[in] tokens_usados Número de tokens utilizados en el texto 
    @param[in] precio_por_1000_tokens Precio por 1000 tokens (por defecto 0.004) 
    @return Coste del texto según el número de tokens devueltos por la IA
    """
    return (tokens_usados / 1000) * precio_por_1000_tokens

# Cargar componentes de conversación y contenido
# Prompts para obtener una pregunta que resuelva la intención de búsqueda
pregunta_sistema = load_component("0. Sistema/0. Pregunta.txt")
pregunta_usuario = load_component("1. Usuario/0. Pregunta.txt")
pregunta_asistente = load_component("2. Asistente/0. Pregunta.txt")

# Prompts para obtener el título del artículo a partir de la palabra clave
titulo_sistema = load_component("0. Sistema/1. Titulo.txt")
titulo_usuario = load_component("1. Usuario/1. Titulo.txt")
titulo_asistente = load_component("2. Asistente/1. Titulo.txt")

# Prompts para generar puntos clave en los que hablar en el artículo
investigacion_sistema = load_component("0. Sistema/2. Investigacion.txt")
investigacion_usuario = load_component("1. Usuario/2. Investigacion.txt")
investigacion_asistente = load_component("2. Asistente/2. Investigacion.txt")

# Prompts para obtener una estructura del artículo
estructura_sistema = load_component("0. Sistema/3. Estructura.txt")
estructura_usuario = load_component("1. Usuario/3. Estructura.txt")
estructura_asistente = load_component("2. Asistente/3. Estructura.txt")

# Prompts para obtener el artículo a partir de la estructura y del título
articulo_sistema = load_component("0. Sistema/4. Articulo.txt")
articulo_usuario = load_component("1. Usuario/4. Articulo.txt")
articulo_asistente = load_component("2. Asistente/4. Articulo.txt")

# Prompts para obtener la descripción para las SERPs de Google
descripcion_sistema = load_component("0. Sistema/5. Descripcion.txt")
descripcion_usuario = load_component("1. Usuario/5. Descripcion.txt")
descripcion_asistente = load_component("2. Asistente/5. Descripcion.txt")

# Prompts para obtener la descripción de la imagen para su generación con iA en aplicaciones externas.
imagen_sistema = load_component("0. Sistema/6. Imagen.txt")
imagen_usuario = load_component("1. Usuario/6. Imagen.txt")
imagen_asistente = load_component("2. Asistente/6. Imagen.txt")

# Prompts para obtener la categoría del artículo
categoria_sistema = load_component("0. Sistema/7. Categoria.txt")
categoria_usuario = load_component("1. Usuario/7. Categoria.txt")
categoria_asistente = load_component("2. Asistente/7. Categoria.txt")

#Prompt para generar la imagen del artículo
promptImg_sistema = load_component("0. Sistema/8. PromptImg.txt")
# Variables globales
total_keywords = len(keywords)
api_valueserp_actual = 0
api_openai_actual = 0
contador_keywords = 0


# Función para realizar una conversación con OpenAI
def chatGPT(sistema, usuario, asistente):
    """
    @brief Realiza una conversación con OpenAI.

    @param sistema El sistema de la conversación.
    @param usuario El mensaje del usuario.
    @param asistente El mensaje del asistente.

    @return La respuesta de OpenAI.

    @note Esta función utiliza la API de OpenAI para realizar una conversación.
    Se utiliza un modelo de lenguaje GPT-3.5-turbo-16k con una temperatura de 0.1.
    En caso de error, se vuelve a intentar con la siguiente clave API.
    """
    global api_openai_actual
    while True:
        api_openai_actual = (api_openai_actual + 1) % len(apis_openai)
        openai.api_key = apis_openai[api_openai_actual]
        try:
            respuesta = openai.chat.completions.create(
                model="gpt-3.5-turbo-16k",
                messages=[
                    {"role": "system", "content": sistema},
                    {"role": "user", "content": usuario},
                    {"role": "assistant", "content": asistente}
                ],
                temperature=0.1
            )
            content = respuesta.choices[0].message.content
            content_strip = content.strip()
            tokens=calcular_numero_tokens(sistema+usuario+asistente+content_strip)
            precio=calcular_coste(tokens)
            return content_strip, precio
        except Exception:
            pass


# Función para obtener resultados de ValueSERP
def obtenerValueSERP(keyword):
    """
    @brief Obtiene resultados de ValueSERP para una palabra clave.
    @param keyword La palabra clave para buscar en ValueSERP.
    @return Los resultados de la búsqueda en ValueSERP.
    @note Esta función utiliza la API de ValueSERP para obtener resultados de búsqueda.
        Se utiliza una lista de claves API para evitar errores de rate limiting.
        En caso de error, se vuelve a intentar con la siguiente clave API.

    """
    global api_valueserp_actual
    while True:
        apiKey = apis_valueserp[api_valueserp_actual]
        parametros = {
            'api_key': apiKey,
            'q': keyword,
            'gl': "es",
            'hl': "es"
        }
        url = 'https://api.valueserp.com/search'
        try:
            response = requests.get(url, params=parametros, timeout=60)
            response_json = response.json()
            resultado = response_json.get('organic_results', [])
            return resultado
        except Exception as e:
            api_valueserp_actual = (api_valueserp_actual + 1) % len(apis_valueserp)

# Función para descargar y analizar un artículo
def descargar_articulo(articulo : Article):
    """
    @brief función que se encarga de descargar y analizar un artículo de una fuente de noticias utilizando la API de ValueSERP.

    @param articulo El artículo a descargar y analizar.

    @note Esta función descarga el contenido del artículo y lo analiza utilizando las funciones download() y parse() del objeto Article. En caso de error, se ignora la excepción y se continúa con la ejecución.
    """
    try:
        articulo.download()
        articulo.parse()
    except Exception as e:
        pass

# Función para leer las keywords existentes de un archivo CSV
def leer_keywords_existentes(nombre_archivo):
    """ 
    @brief La función lee las keywords existentes desde un archivo CSV y las devuelve como un conjunto.
    @param nombre_archivo Ruta del archivo CSV que contiene las keywords
    @return Conjunto de keywords existentes sin duplicados.
    @note La función devuelve un conjunto vacío si el archivo no existe.
    """
    if not os.path.isfile(nombre_archivo):
        return set()
    with open(nombre_archivo, "r", newline="", encoding="utf-8") as archivo_csv:
        lector = csv.reader(archivo_csv)
        next(lector, None)
        keywords_set = {fila[0] for fila in lector}
        return keywords_set
    
# Función para crear una pregunta

def crear_pregunta(keyword : str, titulos : list):
    """
    @brief Crea una pregunta a partir de una palabra clave y un listado de títulos. La pregunta responderá a la intención de búsqueda de la palabra clave.
    @param keyword palabra clave relacionada con la pregunta.
    @param titulos Lista de títulos relacionados con la pregunta. Títulos obtenidos de la API ValueSerps correspondientes a las 10 primeras posiciones de Google.
    @return Una pregunta formateada para ontener información de la intención de búsqueda.
    @note La pregunta se crea utilizando los prompts pregunta_sistema, pregunta_usuario y pregunta_asistente.
    """
    pregunta,precio= chatGPT(pregunta_sistema.format(keyword=keyword), pregunta_usuario.format(titulos=titulos), pregunta_asistente)
    return pregunta,precio


# Función para crear un título
def crear_titulo(pregunta : str, keyword : str, titulos : list):
    """
    @brief Crea un título para una pregunta utilizando el modelo de lenguaje ChatGPT.

    @param pregunta Pregunta relacionada con la keyword.
    @param keyword Palabra clave.
    @param titulos Lista de títulos relacionados con la pregunta. Títulos obtenidos de la API ValueSerps correspondientes a las 10 primeras posiciones de Google.
    @return Un título para un artículo a partir de la información dada optimizado para los búcadores e ideal para la visualización en las SERPs.

    @note La función utiliza los prompts titulo_sistema, titulo_usuario y titulo_asistente para crear el título. Si el título es demasiado largo, se utiliza un bucle para reducir su tamaño y adaptarlo a las pautas de Google sobre los títulos en las SERPs.
    """

    titulo,precio1= chatGPT(titulo_sistema.format(pregunta=pregunta, keyword=keyword), titulo_usuario.format(titulos=titulos), titulo_asistente)
    titulo = titulo.replace("\"", "").rstrip(".")
    intentos = 0 # Se realizan 3 intentos para verificar que la longitud del título es adecuado para las SERPs de Google (Recomendación SEO)
    precio=precio1
    while len(titulo) > 70 and intentos < 3:
        titulo,precio2 = chatGPT(titulo_sistema.format(pregunta=pregunta, keyword=keyword), f"Haz más pequeño el meta título: \"{titulo}\".", titulo_asistente)
        titulo = titulo.replace("\"", "").rstrip(".")
        precio=precio+precio2
        intentos += 1
    return titulo,precio


# Función para crear una investigación
def crear_investigacion(pregunta, competencia):
    """
    @brief Crea una investigación. Lista de frases que responden a la pregunta a partir de un artículo de las primeras posiciones de google 
    @param pregunta Pregunta que hemos obtenido de la IA que resuelve la intención de búsqueda
    @param competencia Texto con un artículo de las 10 primeras posiciones de Google
    @return Una investigación. Consistente en una lista de frases que responden a la intención de búsqueda (pregunta) a partir de la información que se ofrece en un artículo de las primeras posiciones de google que hemos denominado competencia.
    @note La función utiliza los prompts investigacion_sistema, investigacion_usuario y investigacion_asistente para crear la investigación (lista de puntos que dan respuesta a la pregunta). Los saltos de línea múltiples se reemplazan por un solo salto de línea.
    """
    invest,precio=chatGPT(investigacion_sistema.format(pregunta=pregunta), investigacion_usuario.format(competencia=competencia), investigacion_asistente.format(pregunta=pregunta))
    investigacion = re.sub('\n+', '\n', invest)
    return investigacion,precio


# Función para crear la estructura del artículo

def crear_estructura(pregunta, titulo, investigacion):
    """
    @brief Crea la estructura del artículo en HTML 
    @param pregunta Pregunta del usuario @param titulo Título del artículo @param investigacion Investigación relacionada con la pregunta
    @return Estructura del artículo en formato HTML
    @note La función utiliza la función chatGPT para generar la estructura del artículo.
    """
    estruct,precio=chatGPT(estructura_sistema.format(titulo=titulo), estructura_usuario.format(pregunta=pregunta, investigacion=investigacion), estructura_asistente.format(titulo=titulo))
    estructura = f"<h1>{titulo}</h1>\n\n{estruct}"
    return estructura,precio

# Función para crear el artículo

def crear_articulo(titulo, keyword, estructura, investigacion):
    """
    @brief Crea el artículo completo y optimizado para SEO
    @param titulo Título del artículo generado con IA
    @param keyword Palabra clave del artículo proporcionada
    @param estructura Estructura del artículo genrado con IA a partir de la investigación.
    @param investigacion Investigación relacionada con el artículo optenida de la información de Google
    @return Artículo completo en formato HTML

    @note La función utiliza la función chatGPT para generar el contenido del artículo a partir de la pqlqbra clave, la intención de búsqueda (titulo), la estructura en HTML y la investigación realizada con el contenido de los artículos de las primeras posiciones de google que resuelven esa intención de búsqueda. La función también aplica varias correcciones y reemplazos para mejorar la presentación del artículo, incluyendo: Reemplazar cadenas de texto innecesarias, Corregir mayúsculas y minúsculas, Eliminar títulos y subtítulos innecesarios
    @return El artículo completo y corregido en formato HTML optimizado para los buscadores.
    """
    articulo,precio =  chatGPT(articulo_sistema.format(titulo=titulo, keyword=keyword, estructura=estructura), articulo_usuario.format(investigacion=investigacion), articulo_asistente.format(titulo=titulo))
    articulo = articulo.replace(".</h", "</h")
    articulo = articulo.replace(":</h", "</h")
    articulo = articulo.replace("<h2>Introducción</h2>", "")
    articulo = articulo.replace("<h3>Conclusiones</h3>", "")
    articulo = articulo.replace("<h3>Conclusión</h3>", "")
    articulo = re.sub(r'En (conclusión|resumen), (\w)', lambda match: match.group(2).upper(), articulo)
    articulo = articulo.replace("En conclusión, ", "").replace("En resumen, ", "")
    articulo = re.sub(r'<strong>En (conclusión|resumen),</strong> (\w)', lambda match: match.group(2).upper(), articulo)
    articulo = articulo.replace("<strong>En conclusión,</strong> ", "").replace("<strong>En resumen,</strong> ", "")
    return articulo,precio


# Función para crear la descripción del artículo
def crear_descripcion(keyword, estructura):
    """ 
    @brief Crea la descripción del artículo, utilizando la palabra clave y la estructura del artículo con un tamaño máximo de 150 caracteres adecuado al que aparece en las SERPs de Google.
    @param keyword Palabra clave del artículo @param estructura Estructura del artículo
    @return Descripción del artículo. La función crea la descripción del artículo, utilizando la palabra clave y la estructura del artículo.
    @note La función utiliza la función chatGPT para generar la descripción del artículo. También aplica correcciones para asegurarse de que la descripción tenga un tamaño adecuado, reemplazando comillas dobles y reduciendo la longitud de la descripción si es necesario. Crea la descripción del artículo, con un tamaño máximo de 150 caracteres adecuado al que aparece en las SERPs de Google.

    """
    #Genera el prompt para crear la descripción del artículo
    descripcion,precio = chatGPT(descripcion_sistema.format(keyword=keyword), descripcion_usuario.format(estructura=estructura), descripcion_asistente)
    descripcion = descripcion.replace("\"", "")

    #Asegurar que el tamaño de la descripción es menor de 150 caracteres.
    intentos = 0
    while len(descripcion) > 150 and intentos < 3:
        descripcion,precio2 = chatGPT(descripcion_sistema.format(keyword=keyword), f"Haz más pequeña la meta descripción: \"{descripcion}\".", descripcion_asistente)
        descripcion = descripcion.replace("\"", "")
        precio=precio+precio2
        intentos += 1
    return descripcion,precio

# Función para crear la descripción de la imagen
def crear_imagen(estructura):
    """ 
    @brief Genera un texto que sirve para el SEO y como alt de la imagen que generemos posteriormente con DALLE-3. Esta reelacionado con la estructura del artículo
    @param estructura Estructura del artículo
    @return La descripción de la imagen, lista para ser utilizada.
    @note La función genera una descrpción para generar la imagen. La función también aplica correcciones para eliminar comillas dobles y caracteres innecesarios al final de la descripción.

    """
    
    imagen,precio = chatGPT(imagen_sistema, imagen_usuario.format(estructura=estructura), imagen_asistente)
    imagen = imagen.replace("\"", "").rstrip(".")
    return imagen,precio

# Función para crear la categoría
def crear_categoria(estructura):
    """ 
    @brief Genera la categoría a partir la estructura del artículo. En el prompt se puede dar un listado de posibles categorías
    @param estructura Estructura del artículo.
    @return Categoría del artículo.
    @note La función genera la categoría del artículo según la estructura del artículo, utilizando un prompt a la IA.La función también aplica correcciones para eliminar comillas dobles y caracteres innecesarios al final de la categoría.
    """
    categoria,precio = chatGPT(categoria_sistema, categoria_usuario.format(estructura=estructura), categoria_asistente)
    categoria = categoria.replace("\"", "").rstrip(".")
    return categoria,precio


#Función para buscar un vídeo de youtube a partir de la palabra clave
def buscar_video(keyword):
    """
    @brief Busca el mejor video para una keyword dada. Esta función utiliza la clase VideosSearch para buscar el mejor video que coincide con la keyword proporcionada.Si se encuentra un video, se devuelve el enlace del video. De lo contrario, se devuelve una cadena vacía.
    @param keyword Palabra clave para buscar el video.
    @return Enlace del video encontrado o cadena vacía si no se encontró ningún video.
    """
    try:
        #print(f'Buscando mejor video para la keyword: {keyword}')
        search = VideosSearch(keyword, limit=1, language='es')
        result = search.result()
        result_video = result['result']
        if result_video:
            return result_video[0]['link']
        else:       # No se ha encontrado ningún video para esta keyword.
            return ''
    except:
        return ''


def generar_imagen(prompt, output_dir="images", calidad="standard"):
    """
    @brief Genera una imagen a partir de un prompt utilizando la API de OpenAI y el modelo DALLE-3.
    @param prompt Texto que describe la imagen que se desea generar.
    @param output_dir Directorio donde se guardará la imagen generada. Por defecto es "images".
    @param calidad Calidad de la imagen generada. Puede ser "standard" o "high". Por defecto es "standard".
    @return Tupla que contiene la ruta de la imagen generada y el precio asociado a la generación de la imagen.
    """
    with open("1. OpenAI.txt", 'r') as file:
        API_KEY = file.read().strip()
    client = OpenAI(api_key=API_KEY)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    response = client.images.generate(
        model="dall-e-3",
        prompt=promptImg_sistema.format(keyword=prompt),
        size="1024x1024",
        quality=calidad,
        n=1,
    )
    image_url = response.data[0].url
    image_response = requests.get(image_url)
    img = Image.open(BytesIO(image_response.content))
    width, height = img.size #Cambiamos el tamaño de la imagen para salirnos de los estándares de la generación de imagenes con IA y diferenciarnos.
    left = width * .02
    top = height * .02
    right = width * .98
    bottom = height * .98
    img_cropped = img.crop((left, top, right, bottom))
    prompt_without_accents = unidecode.unidecode(prompt)
    filename = prompt_without_accents.lower().replace(' ', '-')
    image_path = f'images/{filename}.jpg'
    img_cropped.save(image_path, 'JPEG')
    precio=0.04 #El precio de generar una imagen estándar 1024x1024 con DALLE-3
    print(f"Imagen guardada en {image_path}")
    return image_path,precio

# Función principal para procesar una keyword
def procesar_keyword(keyword):
    """ 
    @brief Procesa una keyword y genera un artículo relacionado optimizado para los buscadores añadiendo: Título y descripción optimo para las SERPs, el contenido del artículo respondiendo a la intención de búsqueda de la palabra clave en HTML. Una categoría adecuada al contenido, una descripción de la imagen para poder ser generada por una IA.
    @param keyword Palabra clave a procesar
    @return No devuelve ningún valor, pero escribe la información del artículo en un archivo CSV.
    @note La función utiliza varias funciones para generar los diferentes componentes del artículo. La función utiliza hilos para descargar los artículos de la competencia en google y obtener su contenido. Luego, utiliza las funciones auxiliares para generar el título, investigación, estructura, imagen y categoría del artículo.

    @see obtenerValueSERP @see crear_pregunta @see crear_titulo @see descargar_articulo @see crear_investigacion @see crear_estructura @see crear_articulo @see crear_descripcion @see crear_imagen @see crear_categoria
    """
    global contador_keywords
    resultados_organicos = obtenerValueSERP(keyword)
    titulos = "\n".join([res.get('title', '') for res in resultados_organicos])
    pregunta,PrecioPregunta = crear_pregunta(keyword, titulos)
    titulo,PrecioTitulo = crear_titulo(pregunta, keyword, titulos)
    investigacion = ""
    PrecioInvestigacion=0
    for resultado_organico in resultados_organicos:
        competencia = Article(resultado_organico.get('link', ''))
        hilo_descarga = threading.Thread(target=descargar_articulo, args=(competencia,))
        hilo_descarga.start()
        hilo_descarga.join(timeout=60)
        if not hilo_descarga.is_alive():
            competencia = competencia.text
            competencia = ' '.join(competencia.split()[:3000])
            if competencia:
                investigacion,PrecioI = crear_investigacion(pregunta, competencia)
                #investigacion=investigacion+invest
        if not investigacion:
            investigacion = pregunta
        PrecioInvestigacion=PrecioInvestigacion+PrecioI
    estructura,PrecioEstructura = crear_estructura(pregunta, titulo, investigacion)
    articulo,PrecioArticulo = crear_articulo(titulo, keyword, estructura, investigacion)
    descripcion,PrecioDescripcion = crear_descripcion(keyword, estructura)
    imagen,PrecioImagen = crear_imagen(estructura)
    categoria,PrecioCategoria = crear_categoria(estructura)
    video_url=buscar_video(keyword)
    print("Estoy Aquí")
    img,precioImg=generar_imagen(keyword)
    tokensGenerados=calcular_numero_tokens(titulo+pregunta+investigacion+estructura+articulo+descripcion+imagen+categoria)

    precio=PrecioTitulo+PrecioPregunta+PrecioEstructura+PrecioArticulo+PrecioDescripcion+PrecioImagen+PrecioCategoria+PrecioInvestigacion+calcular_coste_generado(tokensGenerados)+precioImg


    fila = [keyword, titulo, imagen, articulo, descripcion, categoria, video_url, precio,img]

    
    with bloqueo:
        escritor.writerow(fila)
    contador_keywords += 1
    print(f"Progreso: {contador_keywords}/{total_keywords} | Keyword: {keyword} | Título: {titulo} | Precio:{precio}")


"""
PROGRAMA PRINCIPAL
"""
# Leer las keywords existentes en el archivo 3. Articulos.csv y obtener las faltantes
keywords_existentes = leer_keywords_existentes("3. Articulos.csv")
keywords_faltantes = [kw for kw in keywords if kw not in keywords_existentes]
total_keywords = len(keywords_faltantes)

# Abrir el archivo CSV para escribir los resultados
with open("3. Articulos.csv", "a", newline="", encoding="utf-8") as archivo_csv:
    escritor = csv.writer(archivo_csv)
    if archivo_csv.tell() == 0:
        escritor.writerow(["Keyword", "Titulo", "Imagen", "Articulo", "Descripcion", "Categoria","Video_url","Precio","Imagen_url"])
    bloqueo = threading.Lock()

    # Utilizar ThreadPoolExecutor para procesar las keywords y generar los artículos  en paralelo
    with concurrent.futures.ThreadPoolExecutor(max_workers=64) as ejecutor:
        futures = [ejecutor.submit(procesar_keyword, kw) for kw in keywords_faltantes]
        concurrent.futures.wait(futures)


previsualizaHTML.generate_preview() #Creamos el arcgivo HTML de Previsualización de Artículos