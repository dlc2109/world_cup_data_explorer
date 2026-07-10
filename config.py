import os

#BASE_DIR es la ubicación "absoluta" del proyecto, pricnipamente es para evitar errores si se ejecuta desde distintas carpetas

BASE_DIR = os.path.abspath(os.path.dirname(__file__)) #esta es la base directory del proyecto

#ruta del archivo de la base de datos en SQLITE
DBPATH = os.path.join(BASE_DIR, 'data', 'world_cup.db') 

#Directorio donde Flask busca al archivo HTML
TEMPLATES_DIR = (BASE_DIR, 'templates')

#Directorio para los archivos de la carpeta static (assets, images, css, js)
STATIC_DIR = os.path.join(BASE_DIR, 'static')


#EXTRA: Añadi más imágenes como logo y trofeo principalmente por diseño, tienen sus animaciones en css y sus funciones en js 
