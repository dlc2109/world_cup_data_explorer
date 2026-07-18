#  Cambios en World Cup Data Explorer 

## 2026-07-17 - Nuevas Cosas: Funciones de Buscador y Endpoints:

### Añadido
- *Buscador de Equipos por Fase:* Se integró un elemento `<input>` reactivo en la sección de eliminatorias que permite filtrar dinámicamente las tarjetas de partidos por el nombre del equipo seleccionado en tiempo real.
- **Endpoint `/api/search_team` en Python:* Nueva ruta en Flask capaz de consultar concurrentemente estadísticas del equipo tanto en la tabla de clasificaciones (`standings`) como en el histórico de cruces eliminatorios (`partidos_eliminacion`).
- *Endpoint `/api/top_goles` en Python:* Ruta auxiliar encargada de abrir el almacén de datos `knockout.json` y ordenarlos descendentemente utilizando funciones lambda basadas en la suma de goles acumulados (`local_goals + away_goals`).

### Modificado

-- index.html: Añadí el nuevo input de búsqueda justo al lado del selector de fases en la sección de Knockout, manteniendo los mismos estilos para que no se desacomode el diseño.
-- Styles.css: Le di estilos al nuevo buscador (bordes redondeados, colores de fondo y un efecto azul cuando haces clic dentro) y agregué un diseño limpio para cuando no se encuentren partidos.
-- Dashboard.js
-- app.py

### Cuantos errores tuve

No cuento las veces que me duelen los focking ojos debido a un 403 Forbidden, 404 Not Found, ECONNREFUSED y 400 Bad Request

lo dejaré con una foto cuando lo actualice en github por pura paja