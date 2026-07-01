# Fases del proyecto

Este documento es una guía sencilla para organizarnos como equipo
durante el desarrollo del proyecto.

La idea no es reemplazar el PDF del curso, sino tener una referencia
rápida que nos recuerde qué sigue, qué buscamos en cada etapa y cómo
queremos trabajar entre nosotros.

La prioridad será terminar un MVP funcional antes de pensar en mejoras.

------------------------------------------------------------------------

# Fase 1. Preparación del proyecto

Antes de comenzar a programar vamos a dejar todo listo para trabajar con
orden.

-   Leer y entender el PDF.
-   Revisar el alcance del MVP.
-   Preparar el entorno de desarrollo.
-   Instalar las dependencias necesarias.
-   Organizar la estructura del proyecto.
-   Configurar Git y GitHub.
-   Dejar lista la base del repositorio.

**Objetivo:** Empezar con una base clara, organizada y alineada con lo
que realmente pide el proyecto.

------------------------------------------------------------------------

# Fase 2. Construcción del scraper

En esta fase nos vamos a concentrar en obtener los datos desde la fuente principal. La idea no es intentar abarcar todo de una vez, sino comenzar con una prueba controlada que nos permita comprobar que sí podemos conectarnos a la página, localizar la sección correcta y extraer una tabla válida.

El primer paso importante aquí es trabajar con el Grupo D, porque esa es la prueba inicial planteada en el proyecto. Si eso sale bien, ya tendremos una base real para seguir avanzando.

También en esta fase empieza a tomar forma la carpeta scraper/, porque allí vamos a separar mejor el trabajo. Por ejemplo, wikipedia_scraper.py nos sirve para manejar la descarga de páginas y coordinar el flujo general del scraping, parsers.py nos ayuda a localizar la sección Standings y revisar la tabla correcta, y normalizers.py nos empieza a preparar el camino para limpiar o acomodar algunos datos antes de pasarlos a etapas posteriores.

Aunque estos archivos se creen desde esta fase, es normal que algunos se vayan completando poco a poco conforme avancemos. La idea no es tener todo terminado desde el principio, sino ir construyendo cada parte cuando realmente la necesitemos.

Durante esta etapa también vamos a aprender a manejar situaciones que pueden ocurrir en un scraper real, por ejemplo cuando una página no responde, cuando la tabla que buscamos cambia de lugar o cuando la información no viene completa. La idea es que el scraper pueda detectar esos casos y reaccionar de una forma controlada, en lugar de simplemente fallar.

1. wikipedia_scraper.py
          │
          ▼
          
2. parsers.py
          │
          ▼
3. normalizers.py

**Dependencias:** o herramientas de esta fase:

requests para descargar el contenido de la página.
beautifulsoup4 para analizar el HTML, localizar la sección Standings y recorrer la tabla.
lxml como apoyo para el procesamiento de tablas HTML cuando sea necesario.

**Objetivo:** 

Lograr una primera extracción funcional y confiable desde una página real, dejando además organizada la base del scraper para que en las siguientes fases sea mucho más fácil ampliar la funcionalidad y reutilizar el código.


--------------------------------------------------------------------

# Fase 3. Procesamiento y almacenamiento de datos

Aquí vamos a limpiar la información obtenida, organizar columnas,
convertir valores numéricos y preparar los datos para que sean fáciles
de usar.

Primero guardaremos una versión en JSON y luego prepararemos SQLite para
trabajar con una copia local de los datos.

**Dependencias:** pandas, json y sqlite3.

**Objetivo:** Tener datos limpios, consistentes y listos para usar.

--------------------------------------------------------------------

# Fase 4. Generalización del scraper

Cuando el Grupo D funcione correctamente, ampliaremos el scraper al
resto de grupos.

No queremos hacer doce scrapers diferentes; la idea es reutilizar la
misma lógica y mejorar el manejo de errores para que un problema no
detenga todo el proceso.

**Objetivo:** Tener un scraper reutilizable y más robusto.

--------------------------------------------------------------------

# Fase 5. Backend y API

Construiremos la API con Flask para consultar posiciones, equipos y
estadísticas.

En esta etapa ya no deberíamos consultar Wikipedia cada vez. Toda la
información debe salir de los datos almacenados localmente.

**Objetivo:** Tener una API clara y organizada.

------------------------------------------------------------------------

# Fase 6. Frontend y pruebas finales

Aquí construiremos la interfaz para mostrar los datos, aplicar filtros,
buscar selecciones y visualizar estadísticas.

Primero nos aseguraremos de completar el MVP antes de pensar en mejoras
visuales.

**Objetivo:** Entregar un MVP completo y funcional.

------------------------------------------------------------------------

# ¿Cómo vamos a trabajar?

-   Vamos a avanzar fase por fase.
-   No vamos a adelantarnos a funcionalidades que no estén en el PDF.
-   Revisaremos el código antes de unir cambios.
-   Si surge una idea nueva, la anotaremos para después del MVP.
-   Queremos entender lo que hacemos, no solo terminar rápido.
-   Si algo se complica mucho, lo dividiremos en partes más pequeñas.
-   Mantendremos la comunicación para que todos sepamos en qué va el
    proyecto.  
-   Antes de comenzar una fase nueva verificaremos que la anterior esté
    terminada.

------------------------------------------------------------------------

# Dependencias principales

Las iremos utilizando poco a poco conforme avancemos:

-   requests
-   beautifulsoup4
-   pandas
-   lxml
-   flask

------------------------------------------------------------------------

# Cuando terminemos el MVP

Si terminamos todas las fases y todavía tenemos tiempo, podremos pensar
en mejoras como gráficos, nuevas estadísticas u otras funcionalidades.

Pero la prioridad siempre será terminar primero el MVP definido en el
PDF y asegurarnos de que todos entendamos cómo funciona el proyecto.

