import requests


# Paso 1: definimos la URL de la pagina que queremos consultar.
# Primero hacemos esto para indicarle al programa cual sera
# la pagina del Grupo D usada en esta prueba inicial de conexion.
URL = "https://en.wikipedia.org/wiki/2026_FIFA_World_Cup_Group_D"


# Paso 2: definimos los headers.
# En este paso agregamos el User-Agent sugerido por el PDF
# para identificarnos de forma clara ante el servidor.
HEADERS = {"User-Agent": "CoderHubEducationalProject/1.0"}


# Paso 3: hacemos la solicitud HTTP.
# Aqui usamos requests.get() para pedir el HTML de la pagina,
# enviando los headers y un timeout de 20 segundos.
response = requests.get(URL, headers=HEADERS, timeout=20)


# Paso 4: imprimimos el codigo de estado.
# Esto nos ayuda a comprobar si la pagina respondio correctamente.
print("Estado:", response.status_code)


# Paso 5: imprimimos el tamano del HTML recibido.
# Con esto verificamos que llego contenido desde la pagina.
print("Tamano HTML:", len(response.text))


# Paso 6: validamos si hubo error HTTP.
# Si la respuesta fue 404, 500 u otro error, aqui se lanzara
# una excepcion para que el problema no pase desapercibido.
response.raise_for_status()
