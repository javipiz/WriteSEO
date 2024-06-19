"""
@file previsualizarHTML.py
@brief En este archivo se implementan todas las funciones para previsualizar los artículos en formato HTML y ver cómo quedarían
"""

import csv
import os
import urllib.parse

#Creamos la plantilla para el blog de visualización de los artículos.

template = '''
<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <title>Previsualización HTML WriteSEO</title>

    <link rel="canonical" href="https://getbootstrap.com/docs/4.0/examples/blog/">

    <!-- Bootstrap core CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css" integrity="sha384-zCbKRCUGaJDkqS1kPbPd7TveP5iyJE0EjAuZQTgFLD2ylzuqKfdKlfG/eSrtxUkn" crossorigin="anonymous">



    <!-- Custom styles for this template -->
    <link href="https://fonts.googleapis.com/css?family=Playfair+Display:700,900" rel="stylesheet">
<!--    <link href="blog.css" rel="stylesheet">-->
    <style>
        /* stylelint-disable selector-list-comma-newline-after */
        .imagen-derecha {{
            float: right;
            margin: 30px 10px 10px 0;
            width: 300px; /* Ajusta el tamaño según tus necesidades */
            height: auto;
        }}
        .blog-header {{
            line-height: 1;
            border-bottom: 1px solid #e5e5e5;
        }}

        .blog-header-logo {{
            font-family: "Playfair Display", Georgia, "Times New Roman", serif;
            font-size: 2.25rem;
        }}

        .blog-header-logo:hover {{
            text-decoration: none;
        }}

        h1, h2, h3, h4, h5, h6 {{
            font-family: "Playfair Display", Georgia, "Times New Roman", serif;
        }}
        
        h2 {{
            margin-top: 30px;
        }}
        
        h3 {{
            margin-top: 20px;
        }}

        .display-4 {{
            font-size: 2.5rem;
        }}

        @media (min-width: 768px) {{
            .display-4 {{
                font-size: 3rem;
            }}
        }}

        .nav-scroller {{
            position: relative;
            z-index: 2;
            height: 2.75rem;
            overflow-y: hidden;
        }}

        .nav-scroller .nav {{
            display: -webkit-box;
            display: -ms-flexbox;
            display: flex;
            -ms-flex-wrap: nowrap;
            flex-wrap: nowrap;
            padding-bottom: 1rem;
            margin-top: -1px;
            overflow-x: auto;
            text-align: center;
            white-space: nowrap;
            -webkit-overflow-scrolling: touch;
        }}

        .nav-scroller .nav-link {{
            padding-top: .75rem;
            padding-bottom: .75rem;
            font-size: .875rem;
        }}

        .card-img-right {{
            height: 100%;
            border-radius: 0 3px 3px 0;
        }}

        .flex-auto {{
            -ms-flex: 0 0 auto;
            -webkit-box-flex: 0;
            flex: 0 0 auto;
        }}

        .h-250 {{
            height: 250px;
        }}

        @media (min-width: 768px) {{
            .h-md-250 {{
                height: 250px;
            }}
        }}

        .border-top {{
            border-top: 1px solid #e5e5e5;
        }}

        .border-bottom {{
            border-bottom: 1px solid #e5e5e5;
        }}

        .box-shadow {{
            box-shadow: 0 .25rem .75rem rgba(0, 0, 0, .05);
        }}

        /*
         * Blog name and description
         */
        .blog-title {{
            margin-bottom: 0;
            font-size: 2rem;
            font-weight: 400;
        }}

        .blog-description {{
            font-size: 1.1rem;
            color: #999;
        }}

        @media (min-width: 40em) {{
            .blog-title {{
                font-size: 3.5rem;
            }}
        }}

        /* Pagination */
        .blog-pagination {{
            margin-bottom: 4rem;
        }}

        .blog-pagination > .btn {{
            border-radius: 2rem;
        }}

        /*
         * Blog posts
         */
        .blog-post {{
            margin-bottom: 4rem;
        }}

        .blog-post-title {{
            margin-bottom: .25rem;
            font-size: 2.5rem;
        }}

        .blog-post-meta {{
            margin-bottom: 1.25rem;
            color: #999;
        }}

        /*
         * Footer
         */
        .blog-footer {{
            padding: 2.5rem 0;
            color: #999;
            text-align: center;
            background-color: #f9f9f9;
            border-top: .05rem solid #e5e5e5;
        }}

        .blog-footer p:last-child {{
            margin-bottom: 0;
        }}
    </style>

</head>

<body>

<div class="container">
    <header class="blog-header py-3">
        <div class="row flex-nowrap justify-content-between align-items-center">
            <div class="col-4 pt-1">
                <a class="text-muted" href="#">UNIR TFG</a>
            </div>
            <div class="col-4 text-center">
                <a class="blog-header-logo text-dark" href="#">WriteSEO</a>
            </div>
            <div class="col-4 d-flex justify-content-end align-items-center">
                <a class="text-muted" href="#">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                        class="mx-3">
                        <circle cx="10.5" cy="10.5" r="7.5"></circle>
                        <line x1="21" y1="21" x2="15.8" y2="15.8"></line>
                    </svg>
                </a>
                <a class="btn btn-sm btn-outline-secondary" href="#">:D</a>
            </div>
        </div>
    </header>

    <div class="nav-scroller py-1 mb-2">
        <nav class="nav d-flex justify-content-between">
            <a class="p-2 text-muted" href="#">Inteligencia Artificial</a>
            <a class="p-2 text-muted" href="#">SEO</a>
            <a class="p-2 text-muted" href="#">Generación de Contenido</a>
            <a class="p-2 text-muted" href="#">NPL</a>
            <a class="p-2 text-muted" href="#">Automatización</a>
            <a class="p-2 text-muted" href="#">GPT3.5 Turbo 16k</a>
            <a class="p-2 text-muted" href="#">WriteSEO</a>
            <a class="p-2 text-muted" href="#">Javi Pizarro</a>
            <a class="p-2 text-muted" href="#">TFG</a>
            <a class="p-2 text-muted" href="#">UNIR</a>
            <a class="p-2 text-muted" href="#">HTML</a>
        </nav>
    </div>

    <div class="jumbotron p-3 p-md-5 text-white rounded bg-dark">
        <div class="col-md-12 px-0">
            <h1 class="display-4 font-italic">Previsualización de Artículos</h1>
            <p class="lead my-3">En esta página listaremos todos los posts que ha generado el script WriteSEO de Javi Pizarro para UNIR.</p>
        </div>
    </div>
</div>

<main role="main" class="container">
    <div class="row">
        <div class="col-md-8 blog-main">
            <h3 class="pb-3 mb-4 font-italic border-bottom">
                TFG UNIR JAVI PIZARRO
            </h3>

            {posts}
            

            <nav class="blog-pagination">
                <a class="btn btn-outline-primary" href="#">Older</a>
                <a class="btn btn-outline-secondary disabled" href="#">Newer</a>
            </nav>

        </div><!-- /.blog-main -->

        <aside class="col-md-4 blog-sidebar">
            <div class="p-3 mb-3 bg-light rounded">
                <h4 class="font-italic">Sobre WriteSEO</h4>
                <p class="mb-0">Este proyecto tiene como objetivo el desarrollo de un script que emplea inteligencia artificial para generar artículos optimizados para buscadores, siguiendo las mejores prácticas de SEO (Search Engine Optimization). La finalidad es crear una herramienta automatizada que facilite la redacción de contenido web de alta calidad, mejorando la visibilidad en motores de búsqueda como Google.</p>
                <p class="mb-0">El enfoque de este trabajo no se limita a un propósito específico, sino que establece las bases para futuras adaptaciones y mejoras. A partir del análisis y desarrollo presentados, se podrán realizar los ajustes necesarios y aprovechar la capacidad de escalabilidad y adaptación que ofrece la inteligencia artificial, permitiendo su aplicación en diferentes contextos empresariales y personales. Durante el desarrollo de este TFG, se integrarán diversas tecnologías y algoritmos de inteligencia artificial, junto con herramientas de software libre, para construir un sistema funcional y escalable. Este sistema permitirá a los usuarios generar contenido optimizado, reduciendo el tiempo y los recursos necesarios para crear artículos de calidad, y mejorando la eficacia en la implementación de estrategias SEO.</p>
                <p class="mb-0">La propuesta incluye el análisis y aplicación de técnicas avanzadas de procesamiento del lenguaje natural (NLP) y aprendizaje automático (ML). Estas técnicas se integrarán en un flujo de trabajo automatizado que garantizará la generación de texto coherente y relevante, ajustado a las mejores prácticas de SEO. Entre estas prácticas se encuentran el uso adecuado de palabras clave, la correcta estructura del contenido y la optimización de metaetiquetas.Este proyecto pretende ofrecer una solución innovadora y eficiente para la generación de contenido web optimizado mediante el uso de inteligencia artificial. Esto contribuirá a mejorar la presencia en línea de empresas y particulares, facilitando la creación de artículos que cumplen con los estándares de calidad y visibilidad en buscadores</p>
            </div>

        </aside><!-- /.blog-sidebar -->

    </div><!-- /.row -->

</main><!-- /.container -->

<footer class="blog-footer">
    <p>WriteSEO 2024
    </p>
    <p>
        <a href="#">Volver arriba</a>
    </p>
</footer>

<!-- Bootstrap core JavaScript
================================================== -->
<!-- Placed at the end of the document so the pages load faster -->
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
        integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
        crossorigin="anonymous"></script>
<script>window.jQuery || document.write('<script src="../../assets/js/vendor/jquery-slim.min.js"><\/script>')</script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-pprn3073KE6tl6bjs2QrFaJGz5/SUsLqktiwsUTF55Jfv3qYSDhgCecCxMW52nD2" crossorigin="anonymous"></script>

<script src="https://cdnjs.cloudflare.com/ajax/libs/holder/2.9.8/holder.min.js"></script>
<script>
    Holder.addTheme('thumb', {{
        bg: '#55595c',
        fg: '#eceeef',
        text: 'Imagen'
    }});
</script>
</body>
</html>
'''



def count_words(s):
    """
    @brief Cuenta el número de palabras en una cadena de texto.
    Divide la cadena de texto en palabras utilizando espacios como separadores y devuelve el número de palabras encontradas.
    @param s Cadena de texto que se desea contar las palabras.
    @return Número de palabras en la cadena de texto.
    """
    return len(s.split())


def generate_post(title, content,imagen, video_url,category,keyword,describe,precio,img):
    
    """
    @brief Genera un post de blog con título, contenido, imagen, video, categoría, palabras clave, descripción y precio.Crea un post de blog con la información proporcionada y devuelve el HTML correspondiente.
    @param title Título del post de blog.
    @param content Contenido del post de blog.
    @param imagen URL de la imagen asociada al post de blog.
    @param video_url URL del video de YouTube asociado al post de blog.
    @param category Categoría del post de blog.
    @param keyword Palabras clave del post de blog.
    @param describe Descripción del post de blog.
    @param precio Precio del artículo asociado al post de blog.
    @param img URL de la imagen asociada al post de blog.
    @return HTML del post de blog generado. 
    """
    yt_code = video_url.replace("https://www.youtube.com/watch?v=", "")
    iframe = f"""<iframe width="750" height="400" src="https://www.youtube.com/embed/{yt_code}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
    """
    if video_url:
        return f'''
                <div class="blog-post">
                    <h1 class="blog-post-title">{title}</h1>
                    <p class="blog-post-meta">30 de Junio, 2024 por <a href="#">Javi Pizarro</a> Categorías: {category} Palabras Clave Usada: {keyword}</p>
                    <p class="blog-post-meta"> <a href="#">Imagen: </a> {imagen} </p>
                    <p class="blog-post-meta"> <a href="#">Descripcion: </a> {describe} </p>


                    {iframe}

                    <p><img src="{img}" alt="{imagen}" class="imagen-derecha">{content}</p>
                </div><!-- /.blog-post -->
                </p>Número de palabras totales: <span class="badge badge-primary">{count_words(content)}</span> Precio del Artículo: <span class="badge badge-primary">{precio} € </span></p>
                <hr>
        '''
    else:
        return f'''
                    <div class="blog-post">
                        <h1 class="blog-post-title">{title}</h1>
                        <p class="blog-post-meta">30 de Junio, 2024 por <a href="#">Javi Pizarro</a> Categorías: {category} Palabras Clave Usada: {keyword}</p>
                        <p class="blog-post-meta"> <a href="#">Imagen: </a> {imagen} </p>
                        <p class="blog-post-meta"> <a href="#">Descripcion: </a> {describe} </p>
                        <p><img src="{img}" alt="{imagen}" class="imagen-derecha">{content}</p>
                    </div><!-- /.blog-post -->
                    </p>Número de palabras totales: <span class="badge badge-primary">{count_words(content)}</span> Precio del Artículo: <span class="badge badge-primary">{precio}</span></p>
                    <hr>
                '''

def generate_preview():
    """
    @brief Genera una vista previa de los posts de blog.
    Lee un archivo CSV que contiene la información de los posts de blog, genera el HTML para cada post utilizando la función generate_post y escribe el resultado en un archivo HTML llamado "preview.html".
    @return None
    """ 
    posts = ''
    with open('3. Articulos.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f, delimiter=',')
        reader.__next__()
        for row in reader:
            keyword=row[0]
            Titulo = row[1]
            Imagen = row[2]
            Articulo=row[3]
            Descripcion=row[4]
            Categoria=row[5]
            video_url =row[6]
            Precio=row[7]
            Img=row[8]
            
            posts = posts + generate_post(Titulo, Articulo,Imagen, video_url,Categoria,keyword,Descripcion,Precio,Img)
    with open('preview.html', 'w', encoding='utf-8-sig') as f:
        f.write(template.format(posts=posts))

    directory = os.getcwd()
    url = os.path.join(directory, 'preview.html').replace('\\', '/').replace(' ', '%20')
    print(f"\n<> <> CLICK PARA PREVISUALIZAR LOS POSTS: file:///{url} <> <>")


if __name__ == '__main__':
    generate_preview()