# Importa el módulo MongoClient de pymongo para interactuar con MongoDB
from pymongo import MongoClient
# Importa pandas, una biblioteca para la manipulación de datos
import pandas as pd
# Importa json para trabajar con datos en formato JSON
import json
# Importa os para realizar operaciones con el sistema de archivos
import os
# Importa datetime para manejar fechas y horas
import datetime

# Función para "aplanar" un diccionario anidado, convirtiendo las claves anidadas en claves únicas
def flatten_dict(d, parent_key='', sep='_'):
    items = {}  # Diccionario para almacenar los elementos aplanados
    for k, v in d.items():
        # Genera una nueva clave combinando la clave actual con la clave del padre usando el separador
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):  # Si el valor es otro diccionario, llama a la función recursivamente
            items.update(flatten_dict(v, new_key, sep=sep))
        else:
            items[new_key] = v  # Si no es un diccionario, añade el valor al nuevo diccionario
    return items

# Configuración de la conexión a la base de datos MongoDB
DB_NAME = "declaranet"            # Nombre de la base de datos
HOST = "148.216.25.182"           # Dirección del host donde se encuentra la base de datos
PASSWORD = "c0ntr4l0r14"          # Contraseña para autenticarse en la base de datos
PORT = 27017                      # Puerto por defecto para MongoDB
USERNAME = "declaranetusr"        # Nombre de usuario para autenticarse en la base de datos

# Creación de la URI de conexión para MongoDB
uri = f"mongodb://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
# Creación de un cliente para conectarse a la base de datos
client = MongoClient(uri)

# Carga un archivo JSON que contiene el pipeline de agregación
with open('pipeline.json', 'r') as file:
    pipeline = json.load(file)

# Vuelve a crear el cliente de MongoDB y selecciona la base de datos y la colección
client = MongoClient(uri)
db = client[DB_NAME]
collection = db['datosPublicos100']  # Nombre de la colección donde se realizará la consulta

# Ejecuta una consulta de agregación en la colección usando el pipeline cargado
cursor = collection.aggregate(pipeline, allowDiskUse=True)
# Convierte los resultados de la consulta en una lista
lista = list(cursor)
# Convierte la lista de resultados en un DataFrame de pandas
df = pd.DataFrame(lista)

# Aplana la columna 'declaracion' del DataFrame para convertir los datos anidados en un formato plano
df_flat = df['declaracion'].apply(lambda x: flatten_dict(x)).apply(pd.Series)
# Concatena el DataFrame original sin la columna 'declaracion' con el DataFrame aplanado
df = pd.concat([df.drop(['declaracion'], axis=1), df_flat], axis=1)

# Obtiene la fecha y hora actuales
fecha_actual = datetime.datetime.now()
# Formatea la fecha actual para usarla como nombre de carpeta
nombre_carpeta = fecha_actual.strftime("%d_%m_%Y")
# Obtiene la ruta del directorio actual
ruta_actual = os.getcwd()

# Crea la ruta completa donde se guardará el archivo CSV
ruta_completa = os.path.join(ruta_actual, nombre_carpeta)

# Verifica si la carpeta existe; si no, la crea
if not os.path.exists(ruta_completa):
    os.makedirs(ruta_completa)

print("Listo")  # Imprime un mensaje indicando que el proceso ha finalizado

# Define el nombre del archivo CSV que se va a guardar
nombre_archivo_csv = "archivo1.csv"
# Crea la ruta completa para el archivo CSV
ruta_archivo_csv = os.path.join(ruta_completa, nombre_archivo_csv)

# Guarda el DataFrame en un archivo CSV en la ubicación especificada
df.to_csv(ruta_archivo_csv, index=False)

