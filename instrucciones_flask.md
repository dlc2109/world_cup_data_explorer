===========================================
FASE FLASK - GUÍA DE IMPLEMENTACIÓN
===========================================

El scraper ya está terminado.

Flujo del proyecto:

Wikipedia
    ↓
wikipedia_scraper.py
    ↓
parsers.py
    ↓
normalizers.py
    ↓
data/standings.json
    ↓
database.py (SQLite)
    ↓
Flask (app.py)
    ↓
Frontend (HTML / JavaScript)

IMPORTANTE

Flask NO debe volver a descargar datos de Wikipedia.

Flask NO debe ejecutar nuevamente el scraper.

Flask debe leer únicamente desde SQLite utilizando las funciones ya creadas.

===========================================
IMPORTS DISPONIBLES
===========================================

Desde scraper.database importar:

from scraper.database import (
    count_standings,
    get_all_standings,
    get_standings_by_group
)

Estas funciones ya funcionan correctamente.

count_standings()
    Devuelve el total de equipos registrados.

get_all_standings()
    Devuelve todos los equipos almacenados.

get_standings_by_group(group_name)
    Devuelve únicamente los equipos del grupo solicitado.

===========================================
RUTAS SUGERIDAS
===========================================

GET /

Página principal.

-------------------------------------------

GET /api/standings

Debe devolver todos los standings.

Internamente utilizar:

get_all_standings()

-------------------------------------------

GET /api/standings?group=D

Debe devolver únicamente el grupo solicitado.

Internamente utilizar:

get_standings_by_group(group_name)

-------------------------------------------

GET /api/statistics

Debe devolver estadísticas generales.

Inicialmente:

{
    "total_records": count_standings()
}

===========================================
NO MODIFICAR
===========================================

No modificar:

scraper/
    wikipedia_scraper.py

scraper/
    parsers.py

scraper/
    normalizers.py

scraper/
    database.py

Todas esas funciones ya fueron probadas.

===========================================
OBJETIVO DE ESTA FASE
===========================================

El trabajo de Flask consiste únicamente en:

1. Recibir una petición HTTP.
2. Llamar a las funciones de database.py.
3. Devolver la respuesta al navegador en formato JSON.

No volver a realizar scraping.

No leer Wikipedia.

No procesar HTML.

No limpiar datos.

Toda esa lógica ya está implementada.
