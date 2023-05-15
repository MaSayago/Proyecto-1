import ast
import pandas as pd
from typing import Union
from fastapi import FastAPI
from datetime import datetime
import json
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import joblib
### Importar el archivo ##############################################
df = pd.read_csv("dataset_Transformado.csv", sep=";")


#Creacion de la API
app = FastAPI()

df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

#Primera ruta 
@app.get('/peliculas_mes/{mes}')
def peliculas_mes(mes:str):
    '''Esta funcion retorna la cantidad de peliculas que se estrenaron en el mes(str) ingresado'''

    #Traduccion del imput en int
    if mes.lower() == "enero":
        mseleccion = 1
    elif mes.lower() == "febrero":
        mseleccion = 2
    elif mes.lower() == "marzo":
        mseleccion = 3
    elif mes.lower() == "abril":
        mseleccion = 4
    elif mes.lower() == "mayo":
        mseleccion = 5
    elif mes.lower() == "junio":
        mseleccion = 6
    elif mes.lower() == "julio":
        mseleccion = 7
    elif mes.lower() == "agosto":
        mseleccion = 8
    elif mes.lower() == "septiembre":
        mseleccion = 9
    elif mes.lower() == "octubre":
        mseleccion = 10
    elif mes.lower() == "noviembre":
        mseleccion = 11
    elif mes.lower() == "diciembre":
        mseleccion = 12
    
    # Contar los valores únicos de la columna 'title' para el int prodcuto del imput
    cantidad = df[df["release_date"].dt.month == mseleccion]['title'].nunique()
    
    # Retornar los resultados
    return {'mes':mes, 'cantidad':cantidad}


@app.get('/peliculas_dis/{dis}')
def peliculas_dia(dia: str):
    '''Esta funcion retorna la cantidad de peliculas que se estrebaron el dia (AAAA-mm-dd) ingresado'''
    
    #Contar la cantidad de "titles" en "release_date"
    cantidad = df[df["release_date"] == dia]['title'].nunique()
    
    # Retornar los resultados
    return {'dia': dia, 'cantidad': cantidad}


@app.get('/franquicia/{franquicia}')
def franquicia(franquicia: str):
    '''Esta funcion retorna la cantidad de peliculas, ganancia total y promedio de la franquicia(str) ingresada'''
    # Filtrar el DataFrame por el nombre de la franquicia
    filtered_df = df[df['collection_name']== franquicia]

    # Obtener la cantidad de películas de la franquicia
    cantidad = filtered_df.shape[0]

    # Calcular la ganancia total y promedio de la franquicia
    ganancia_total = filtered_df['revenue'].sum()
    ganancia_promedio = filtered_df['revenue'].mean()
    
    # Guardar la respuesta en una variable tranformando los valores numericos a str
    respuesta = {"franquicia": franquicia, "cantidad": str(cantidad),
                    "ganancia_total": str(ganancia_total), "ganancia_promedio": str(ganancia_promedio)}
    

    # Retornar los resultados
    return respuesta


@app.get('/peliculas_pais/{pais}')
def peliculas_pais(pais: str):
    '''Esta función retorna la cantidad de películas producidas en el país(str) ingresado'''

    # Convertir la columna 'production_countries' en una lista de listas de países
    df['production_countries'] = df['production_countries'].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else [])

    # Filtrar el DataFrame por el país
    filtered_df = df[df['production_countries'].apply(lambda x: pais in x)]

    # Obtener la cantidad de películas producidas en el país
    cantidad = filtered_df.shape[0]

    # Retornar los resultados
    return {'pais': pais, 'cantidad': cantidad}


@app.get('/productoras/{productora}')
def productoras(productora: str):
    '''Esta funcion retornando la ganancia toal y la cantidad de peliculas de la prodcutora(str) ingresada'''
    # Filtrar el DataFrame por la prodcutora
    productoras_df = df[df['company_names'].apply(lambda x: productora in x)]
    
    #Obtener la ganancia total
    ganancia_total = productoras_df['revenue'].sum()
    
    #Obtener la cantidad
    cantidad = productoras_df.shape[0]
    
    #Guardar la respuesta en una variable tranformando los valores numericos a str
    respuesta = {'productora': str(productora),
                     'ganancia_total': str(ganancia_total), 'cantidad': str(cantidad)}

    # Retornar los resultados
    return respuesta

@app.get('/retorno/{pelicula}')
def retorno(pelicula: str):
    
    '''Esta funcion retorna la inversion, la ganancia, el retorno y el año en el que se lanzo la pelicula(str) ingresada'''
    # Filtrar el DataFrame para obtener la película especificada
    pelicula_df = df[df['title'] == pelicula]

    # Obtener la inversión, ganancia, retorno y año de lanzamiento de la película
    inversion = pelicula_df['budget'].values[0]
    ganancia = pelicula_df['revenue'].values[0]
    retorno = pelicula_df['return'].values[0]
    año_lanzamiento = pelicula_df['release_year'].values[0]

    # Guardar la respuesta en una variable tranformando los valores numericos a str
    respuesta = {'pelicula': str(pelicula), 'inversion': str(inversion),
                 'ganancia': str(ganancia), 'retorno': str(retorno), 'año': str(año_lanzamiento)}

    # Retornar los resultados
    return respuesta

from sklearn.neighbors import NearestNeighbors
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler


# Paso 3: Convertir las columnas con listas de cadenas en listas de Python
df['production_countries'] = df['production_countries'].apply(
    ast.literal_eval)
df['company_names'] = df['company_names'].apply(ast.literal_eval)
df['company_ids'] = df['company_ids'].apply(ast.literal_eval)
df['genre_names'] = df['genre_names'].apply(ast.literal_eval)

# Paso 4: Seleccionar las características relevantes para el modelo de recomendación y realizar la imputación de valores faltantes
features = ['budget', 'popularity', 'revenue', 'runtime', 'vote_average']
X = df[features]

imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X_imputed)

# Paso 5: Construir el modelo de k-NN
model = NearestNeighbors()
model.fit(X_scaled)

@app.get('/recomendacion/{titulo}')
def recomendacion(titulo:str):
    '''Ingresas un nombre de pelicula y te recomienda las similares en una lista'''
    # Buscar el índice de la película según el título
    movie_index = df[df['title'] == titulo].index[0]

    # Convertir el vector de características en un arreglo bidimensional
    X_movie = X_scaled[movie_index].reshape(1, -1)

    # Obtener las películas recomendadas utilizando el modelo de k-NN
    distances, indices = model.kneighbors(X_movie)
    recommended_movies = df.iloc[indices[0]]['title'].tolist()
    
    respuesta = {'1': str(recommended_movies[0]), '2': str(recommended_movies[1]), '3': str(recommended_movies[2]), '4': str(recommended_movies[3]), '5': str(recommended_movies[4])}

    return {'lista recomendada': respuesta }