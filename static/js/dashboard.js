/* ======================================================
    DASHBOARD JS
    Primera conexión entre el Frontend y Flask.

    Flujo:

    SQLite
        ↓
    database.py
        ↓
    app.py
        ↓
    GET /api/statistics
        ↓
    dashboard.js
        ↓
    HTML

    En esta primera fase únicamente consumimos
    la ruta:

        GET /api/statistics

====================================================== */

const STATISTICS_API_URL = "/api/statistics";
const EMPTY_VALUE = "--";


/* ======================================================
    HELPERS
====================================================== */

// Devuelve un elemento del HTML usando su id.
function getElementById(id) {
    return document.getElementById(id);
}

// Cambia el texto de cualquier elemento.
function setElementText(id, value) {
    const element = getElementById(id);

    if (!element) {
        return;
    }

    element.textContent = value ?? EMPTY_VALUE;
}

// Prepara los números antes de mostrarlos.
function formatNumber(value) {

    if (value === null || value === undefined) {
        return EMPTY_VALUE;
    }

    return value.toLocaleString();

}


/* ======================================================
    API
====================================================== */

// Comunicación con Flask usando GET /api/statistics.
async function fetchStatistics() {
    const response = await fetch(STATISTICS_API_URL);

    if (!response.ok) {
        throw new Error(`Error HTTP al cargar estadísticas: ${response.status}`);
    }

    // Convertimos el JSON recibido en un objeto JavaScript.
    return response.json();
}


/* ======================================================
    FECHA
====================================================== */

// Prepara la fecha de actualización antes de mostrarla.
function getUpdateDateParts(updatedAt) {

    let date;

    // Python: datetime.now()
    // JavaScript: new Date()
    if (updatedAt) {

        date = new Date(updatedAt);

    } else {

        date = new Date();

    }

    return {

        // Ejemplo: Jul 05, 2026
        dateText: date.toLocaleDateString(
            "en-US",
            {
                month: "short",
                day: "2-digit",
                year: "numeric",
            }
        ),

        // Ejemplo: 04:45 PM
        timeText: date.toLocaleTimeString(
            "en-US",
            {
                hour: "2-digit",
                minute: "2-digit",
            }
        ),

    };

}


/* ======================================================
    LAST UPDATE
====================================================== */

// Actualiza la tarjeta "Last Update" del dashboard.
function updateLastUpdate(statistics) {

    const updateDate = getUpdateDateParts(
        statistics.updated_at
    );

    setElementText(
        "last_update_date_value",
        updateDate.dateText
    );

    setElementText(
        "last_update_time_value",
        updateDate.timeText
    );

    return updateDate;

}


/* ======================================================
    SIDEBAR
====================================================== */

// Actualiza la fecha de la última actualización en el sidebar.
function updateSidebar(updateDate) {

    setElementText(
        "sidebar_update_value",
        `${updateDate.dateText} - ${updateDate.timeText}`
    );

}


/* ======================================================
    STATISTICS CARDS
====================================================== */

// Actualiza todas las tarjetas usando GET /api/statistics.
function updateStatisticsCards(statistics) {

    // Total de equipos.
    setElementText(
        "total_teams_value",
        formatNumber(statistics.total_records)
    );

    // Total de partidos.
    setElementText(
        "total_matches_value",
        formatNumber(statistics.total_matches)
    );

    // Total de goles.
    setElementText(
        "total_goals_value",
        formatNumber(statistics.total_goals)
    );

    // Promedio de goles.
    setElementText(
        "average_goals_value",
        formatNumber(statistics.average_goals)
    );

    // Mejor ataque.
    setElementText(
        "best_offense_team_value",
        statistics.best_offense_team ?? EMPTY_VALUE
    );

    setElementText(
        "best_offense_goals_value",
        `${formatNumber(statistics.best_offense_goals)} goals scored`
    );

    // Mejor defensa.
    setElementText(
        "best_defense_team_value",
        statistics.best_defense_team ?? EMPTY_VALUE
    );

    setElementText(
        "best_defense_goals_value",
        `${formatNumber(statistics.best_defense_goals)} goals conceded`
    );

    // Last Update + Sidebar.
    const updateDate = updateLastUpdate(statistics);

    updateSidebar(updateDate);

}


/* ======================================================
    INICIO DEL DASHBOARD
====================================================== */

// Inicia la carga de estadísticas.
async function initializeDashboard() {

    try {

        const statistics = await fetchStatistics();

        updateStatisticsCards(statistics);

    } catch (error) {

        console.error("No se pudieron cargar las estadísticas:", error);

    }

}

// Espera a que el HTML exista antes de buscar IDs.
document.addEventListener(
    "DOMContentLoaded",
    initializeDashboard
)