# WriteSEO
Generación masiva de artículos optimizados para los buscadores a partir de palabras clave 
# Introducción
 Este proyecto está diseñado para generar artículos optimizados para los motores de búsqueda con prácticas de SEO de contenidos. Para ello utilizamos Inteligencia Artificial, en concreto, el modelo GPT Turbo 16k de OpenAi. También Utilizamos una API llamada ValueSerps para realizar peticiones a Google y optener cierta información de los contenidos de las primeras posiciones que aparecen al utilizar la palabra clave con la que queremos desarrollar el contenido.
 
 ## Funcionalidades Principales
 - Procesamiento de CSV: Lectura y escritura de archivos CSV y de archivos de texto para la gestión de datos. A destacar los archivos donde introduciremos las palabras clave que queremos desarrollar como artículos, los prompts a la inteligencia artificial para darle forma al contenido y los archivos donde se introduciran las apikey de OpenAI y ValueSerps
 - Interacción con OpenAI: Utilización de la API de OpenAI para generar contenido basado en IA.
 - Interacción con ValueSerp: Utilización de la API de ValueSerp para adquirir información de los contenidos de Google, los principales, a partir de la palabra clave con la que se quiera desarrollar el artículo.
 - Búsqueda y análisis**: Búsqueda de contenido que satisfazga la intención de búsqueda que tiene la palabra clave y análisis de los mismos para generar nuevo contenido que resueva esa intención de búsqueda. Se generará un artículo basado en lo que realmente esta buscando el usuario. Este tipo de contenidos son atractivos para los buscadores y se posicionarán bien.
 - Generación Artículos SEO: Creación de uno o varios Artículos a partir de una palabra clave con un optimo SEO on page. Estos artículos contendrán: Un formato basado en títulos que resuelven la intención de búsqueda, formato HTML, un numero adecuado de palabras relacionadas con la palabra clave, un título SEO atractivo para el usuario y para las SERPs, una descripción SEO atractiva para el usuario y para las SERPs, la asignación de una categoría adecuada a unas pautas previamente dadas, la inclusión de un vídeo relacionado con el contenido del artículo, la generación con IA (DALLE-3) e inserción de una imagen única y su configuración optima para el SEO, el cálculo de el número de palabras del artículo resultante y el cálculo del precio final de cada artículo . 
 - Generación de Imágenes: Creación de imágenes a partir de descripciones textuales utilizando la API de OpenAI.
 - Generación de una Previsualización HTML: Creación de un archivo de previsualización en formato HTML en el que se podrá ver el resultado de los artículos generados.
 
 ## Instalación
 Para instalar y configurar este proyecto, sigue los pasos a continuación:
  1. Clona el repositorio del proyecto.
  2. Instala las dependencias utilizando `pip install -r requirements.txt`.
  3. Configura las claves API necesarias en los archivos correspondientes.
  4. Revisa los archivos de prompts, por defecto te genera todo pero siempre puedes cambiar y probar nuevas instrucciones a la IA.
 
  ## Uso
  Aquí tienes un ejemplo básico de cómo utilizar WriteSEO
  1. Introducir una o un listado de palabras clave. Puede ser mediante un archivo .csv llamado "palabrasclave.csv" en cuya segunda columna tenga las palabras clave o introduciendo en el archivo de texto Keywords.txt las palabras clave.
  2. Ejecutar el Script y esperar a que se generen los artículos.
  3. Visualizar los artículos abriendo preview.html en tu navegador preferido o gestionar los datos generados en el archivo "3. Articulos.csv" con una aplicacion externa.
 
  ## Estructura del Proyecto
  - `procesarcsv.py`: Funciones para procesar la entrada de datos (palabras clve) a partir de un archivo CSV.
  - `previsualizaHTML.py`: Generación de previsualizaciones HTML.
  - `WriteSEO.py`: Script principal que coordina todas las operaciones.
 
  ## Contribuir
  Las contribuciones son bienvenidas. Por favor, sigue las guías de contribución y abre un Pull Request para discutir los cambios propuestos.
 
  ## Licencia
  Este proyecto está bajo la Licencia MIT.

