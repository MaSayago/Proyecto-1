import pandas as pd
import ast
from fastapi import FastAPI
from sklearn.neighbors import NearestNeighbors
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler


### Importar el archivo ##############################################
df = pd.read_csv("dataset_Transformado.csv", sep=";")


#Creacion de la API
app = FastAPI()

df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

### Primer Boton ######################################################
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
    
    # Valores únicos de la columna 'title' para el int prodcuto del imput
    cantidad = df[df["release_date"].dt.month == mseleccion]['title'].nunique()
    
    return {'mes':mes, 'cantidad':cantidad}

### Segundo Boton ######################################################
@app.get('/peliculas_dis/{dis}')
def peliculas_dia(dia: str):
    '''Esta funcion retorna la cantidad de peliculas que se estrebaron el dia (AAAA-mm-dd) ingresado'''
    
    #Contar la cantidad de "titles" en "release_date"
    cantidad = df[df["release_date"] == dia]['title'].nunique()
    
    # Retornar los resultados
    return {'dia': dia, 'cantidad': cantidad}

### Tercer Boton ######################################################
@app.get('/franquicia/{franquicia}')
def franquicia(franquicia: str):
    '''Esta funcion retorna la cantidad de peliculas, ganancia total y promedio de la franquicia(str) ingresada'''
    # Nueva variable a partir del DataFrame por el nombre de la franquicia
    filtered_df = df[df['collection_name']== franquicia]

    # Cantidad de películas de la franquicia
    cantidad = filtered_df.shape[0]

    # Ganancia total y promedio de la franquicia
    ganancia_total = filtered_df['revenue'].sum()
    ganancia_promedio = filtered_df['revenue'].mean()
    
    # Se guarda los valores a retornar en un variable para que no arroje error
    respuesta = {"franquicia": franquicia, "cantidad": str(cantidad),
                    "ganancia_total": str(ganancia_total), "ganancia_promedio": str(ganancia_promedio)}
    
    return respuesta

### Cuarto Boton ######################################################

@app.get('/peliculas_pais/{pais}')
def peliculas_pais(pais: str):
    '''Esta función retorna la cantidad de películas producidas en el país(str) ingresado'''

    # Columna 'production_countries' en una lista de listas de países
    df['production_countries'] = df['production_countries'].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else [])

    # DataFrame de acuerdo al país
    filtered_df = df[df['production_countries'].apply(lambda x: pais in x)]

    # Cantidad de películas producidas
    cantidad = filtered_df.shape[0]

   
    return {'pais': pais, 'cantidad': cantidad}

### Quinto Boton ######################################################
@app.get('/productoras/{productora}')
def productoras(productora: str):
    '''Esta funcion retorna la ganancia total y la cantidad de peliculas de la prodcutora(str) ingresada'''
    # DataFrame por prodcutora
    productoras_df = df[df['company_names'].apply(lambda x: productora in x)]
    
    ganancia_total = productoras_df['revenue'].sum()
    
    #Cantidad
    cantidad = productoras_df.shape[0]
    
    # Se guarda los valores a retornar en un variable para que no arroje error
    respuesta = {'productora': str(productora),
                     'ganancia_total': str(ganancia_total), 'cantidad': str(cantidad)}

    return respuesta

### Sexcto Boton ######################################################
@app.get('/retorno/{pelicula}')
def retorno(pelicula: str):
    
    '''Esta funcion retorna la inversion, la ganancia, el retorno y el año en el que se lanzo la pelicula(str) ingresada'''
    # DataFrame por película especificada
    pelicula_df = df[df['title'] == pelicula]

    # Inversión, ganancia, retorno y año de lanzamiento de la película
    inversion = pelicula_df['budget'].values[0]
    ganancia = pelicula_df['revenue'].values[0]
    retorno = pelicula_df['return'].values[0]
    año_lanzamiento = pelicula_df['release_year'].values[0]

    # Se guarda los valores a retornar en un variable para que no arroje error
    respuesta = {'pelicula': str(pelicula), 'inversion': str(inversion),
                 'ganancia': str(ganancia), 'retorno': str(retorno), 'año': str(año_lanzamiento)}


    return respuesta


### Sexcto Boton ######################################################

variable_de_interes = ['budget', 'popularity',
                       'revenue', 'runtime', 'vote_average']
X = df[variable_de_interes]


imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X_imputed)

# Instanciado del modelo
model = NearestNeighbors()
model.fit(X_scaled)


@app.get('/recomendacion/{titulo}')
def recomendacion(titulo:str):
    '''Esta funcion te recomiendo 5 peliculas en base a la ingresada '''

    # Indice de la película según el título
    movie_index = df[df['title'] == titulo].index[0]

    X_movie = X_scaled[movie_index].reshape(1, -1)

    distances, indices = model.kneighbors(X_movie)
    recommended_movies = df.iloc[indices[0]]['title'].tolist()

    respuesta = {'1': str(recommended_movies[0]), '2': str(recommended_movies[1]), '3': str(
        recommended_movies[2]), '4': str(recommended_movies[3]), '5': str(recommended_movies[4])}

    return {'lista recomendada': respuesta}
