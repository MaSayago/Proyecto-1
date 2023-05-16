
# ***PROYECTO INDIVIDUAL Nº1***

## Descripción del proyecto 

El proyecto consta de realizar un análisis exploratorio de datos de películas, crear una API para acceder a información sobre películas y entrenar un modelo de recomendación basado en similitud de puntuaciones.

## Transfomraciones realizadas

Para este proyecto se trabajó con un archivo CSV  nombrado "movies_dataset.csv" que contenía información sobre películas, como título, año de estreno, presupuesto, ingresos, etc.

Durante el proceso se relizaron las siguientes transformaciones:

* Se desanidaron las columnas "belongs_to_collection", "production_companies", "genres", "production_countries".
* Se reemplazaron por 0 los valores nulos de los campos "revenue" y "budget" se reemplazaron por 0.
* Se eliminaron los valores nulos del campo "release date".
* Se extrajo el año de la fecha de estreno para crear la columna "release_year" y se le dió el formato AAAA-mm-dd a la columna "release_date"
* Se creó la columna "return" para calcular el retorno de inversión.
* Se eliminaron las columnas que no se utilizarían en el análisis o fueron desanidados tales como: "belongs_to_collection", "genres","video", "imdb_id", "adult", "original_title", "vote_count", "poster_path", "homepage", 'id', 'overview', 'production_companies','spoken_languages', 'tagline', 'collection_id', 'poster_path', 'backdrop_path'

Finalmente los datos se exportar la csv "dataset_Transformado.csv"

## Desarrollo de la API

Se desarrollaron 7 endpoints utilizando el framework FastAPI con el fin de consultar información sobre películas. Estos endpoints son:

* /peliculas_mes(mes): Esta funcion retorna la cantidad de peliculas que se estrenaron en el mes(str) ingresado
* /peliculas_dia(dia): Esta funcion retorna la cantidad de peliculas que se estrebaron el dia (AAAA-mm-dd) ingresado
* /franquicia(franquicia): Esta funcion retorna la cantidad de peliculas, ganancia total y promedio de la franquicia(str) ingresada
* /peliculas_pais(pais): Esta función retorna la cantidad de películas producidas en el país(str) ingresado'
* /productoras(productora): Esta funcion retorna la ganancia total y la cantidad de peliculas de la prodcutora(str) ingresada
* /retorno(pelicula): Esta funcion retorna la inversion, la ganancia, el retorno y el año en el que se lanzo la pelicula(str) ingresada
* /recomendacion(titulo)"Esta funcion te recomiendo 5 peliculas en base a la ingresada

## EDA

Se realizó un análisis exploratorio de las variables numericas para investigar las relaciones entre las mismas, se identificaron outliers y se utilizarían para el machine learning. Las variables de interes seleccionadas fueron las siguientes:

* 'budget': El presupuesto de una película puede tener un impacto significativo en su éxito y calidad de producción.
* 'popularity': La popularidad de una película puede influir en su éxito comercial y en la atención que recibe del público.
* 'revenue': Los ingresos generados por una película son un indicador clave de su éxito financiero.
* 'runtime': La duración de una película puede influir en la experiencia del espectador y en la comercialización de la misma.
* 'vote_average': La calificación promedio de votos de una película puede ser un indicador de su calidad y aceptación general.
* 'release_year': El año de lanzamiento de una película puede tener un impacto en su contexto histórico, influencia cultural y relevancia en relación con otras películas del mismo período.
* 'original_language': El idioma original de una película puede ser relevante para el análisis de la industria cinematográfica a nivel global y para comprender las preferencias de audiencia en diferentes regiones y países.

En el archivo nombrado "EDA.jpynb" se pueden apreciar las oberservaciones producto del analisis de la relacion entre dichas variables

## Modelo de recomendación

Se implementó un modelo de recomendación basado en el algoritmo de vecinos más cercanos (K-NN) utilizando la librería scikit-learn. Este modelo utiliza las puntuaciones , la inversion y la ganancias de las películas entre otras variables para calcular la similitud entre ellas y realizar recomendaciones

## Deployment

La API se encuentra desplegada en la plataforma Render, enalsada a través de uvicorn. Puedes acceder a la API a través del siguiente enlace: [link](https://one7-jyvl.onrender.com/docs#/)

## Comentarios finales

Esta iniciativa posibilitó la exploración exhaustiva de diversos elementos en el análisis de datos, el desarrollo de una interfaz de programación de aplicaciones (API) y el entrenamiento de modelos de aprendizaje automático. Se adquirieron datos de relevancia del dataset de películas y se creó una API que destaca por su simplicidad y eficacia para acceder a dicha información.
