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
const STANDINGS_API_URL = "/api/standings";
const EMPTY_VALUE = "--";
const TABLE_COLUMN_COUNT = 11;
// Guarda los standings cargados desde Flask.
// Se reutilizarán para el buscador.
let standingsData = [];

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

// Pausa pequena usada para transiciones visuales.
function wait(milliseconds) {
    return new Promise(function (resolve) {
        window.setTimeout(resolve, milliseconds);
    });
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
    STANDINGS API
====================================================== */

// Comunicación con Flask usando GET /api/standings.
// Comunicación con Flask usando GET /api/standings.
// También puede recibir una URL con filtro, por ejemplo:
// /api/standings?group=A
async function fetchStandings(url) {

    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(`Error HTTP al cargar standings: ${response.status}`);
    }

    return response.json();

}
/* ======================================================
    STANDINGS TABLE
====================================================== */

// Crea una fila HTML para un equipo.
function createStandingRow(team) {

    return `
        <tr>
            <td>${team.position ?? EMPTY_VALUE}</td>
            <td>${team.team ?? EMPTY_VALUE}</td>
            <td>${team.played ?? EMPTY_VALUE}</td>
            <td>${team.wins ?? EMPTY_VALUE}</td>
            <td>${team.draws ?? EMPTY_VALUE}</td>
            <td>${team.losses ?? EMPTY_VALUE}</td>
            <td>${team.goals_for ?? EMPTY_VALUE}</td>
            <td>${team.goals_against ?? EMPTY_VALUE}</td>
            <td>${team.goal_difference ?? EMPTY_VALUE}</td>
            <td>${team.points ?? EMPTY_VALUE}</td>
            <td>${team.qualification ?? EMPTY_VALUE}</td>
        </tr>
    `;

}


/* ======================================================
    TABLE UX STATES
====================================================== */

function getStandingsTableBody() {
    return getElementById("standings_table_body");
}

function showLoading() {
    const tableBody = getStandingsTableBody();

    if (!tableBody) {
        return;
    }

    tableBody.classList.add("table_loading");
    tableBody.innerHTML = `
        <tr>
            <td colspan="${TABLE_COLUMN_COUNT}">
                <div class="table_loading_content">
                    <span class="table_spinner"></span>
                    <span>Loading standings...</span>
                </div>
            </td>
        </tr>
    `;
}

function hideLoading() {
    const tableBody = getStandingsTableBody();

    if (!tableBody) {
        return;
    }

    tableBody.classList.remove("table_loading");
}

function showEmptyState() {
    const tableBody = getStandingsTableBody();

    if (!tableBody) {
        return;
    }

    tableBody.innerHTML = `
        <tr class="empty_state">
            <td colspan="${TABLE_COLUMN_COUNT}">
                <div class="empty_state_content">
                    <svg class="empty_state_icon" viewBox="0 0 24 24" aria-hidden="true">
                        <circle cx="11" cy="11" r="7"></circle>
                        <path d="M16.5 16.5L21 21"></path>
                    </svg>
                    <span class="empty_state_title">No teams found</span>
                    <span class="empty_state_description">
                        Try another search or another group.
                    </span>
                </div>
            </td>
        </tr>
    `;
}

function clearEmptyState() {
    const tableBody = getStandingsTableBody();

    if (!tableBody) {
        return;
    }

    tableBody.innerHTML = "";
}

async function animateTableUpdate(updateCallback) {
    const tableBody = getStandingsTableBody();

    if (!tableBody) {
        return;
    }

    tableBody.classList.add("table_fade");

    await wait(180);

    updateCallback();

    tableBody.classList.remove("table_fade");
}

// Renderiza todos los equipos dentro del tbody.
function renderStandingsTable(standings) {

    const tableBody = getStandingsTableBody();

    if (!tableBody) {
        return;
    }

    if (standings.length === 0) {
        showEmptyState();
        return;
    }

    clearEmptyState();

    let tableRows = "";

    for (const team of standings) {
        tableRows += createStandingRow(team);
    }

    tableBody.innerHTML = tableRows;

}

/* ======================================================
    STANDINGS FILTER
====================================================== */

// Lee el grupo seleccionado en el select del HTML.
//
// HTML:
// <select id="group_filter_select">
function getSelectedGroup() {

    const groupFilter = getElementById("group_filter_select");

    if (!groupFilter) {
        return "";
    }

    return groupFilter.value;

}


// Construye la URL correcta para la API de standings.
//
// Si no hay grupo seleccionado:
//     /api/standings
//
// Si hay grupo seleccionado:
//     /api/standings?group=A
function getStandingsUrl() {

    const selectedGroup = getSelectedGroup();

    let url = STANDINGS_API_URL;

    if (selectedGroup) {
        url = `${STANDINGS_API_URL}?group=${selectedGroup}`;
    }

    return url;

}


function setFilterActive() {
    const groupFilter = getElementById("group_filter_select");

    if (!groupFilter) {
        return;
    }

    if (groupFilter.value) {
        groupFilter.classList.add("filter_active");
    } else {
        groupFilter.classList.remove("filter_active");
    }
}


// Carga standings desde Flask y renderiza la tabla.
async function loadStandings() {

    const url = getStandingsUrl();

    showLoading();

    try {
        standingsData = await fetchStandings(url);

        await animateTableUpdate(function () {
            renderStandingsTable(standingsData);
        });
    } catch (error) {
        console.error("No se pudieron cargar los standings:", error);
        showEmptyState();
    } finally {
        hideLoading();
        setFilterActive();
    }

}


// Activa el evento change del filtro de grupo.
//
// Cuando el usuario cambia el select,
// se vuelve a cargar la tabla con el grupo seleccionado.
function setupGroupFilter() {

    const groupFilter = getElementById("group_filter_select");

    if (!groupFilter) {
        return;
    }

    setFilterActive();

    groupFilter.addEventListener(
        "change",
        function () {
            setFilterActive();
            loadStandings();
        }
    );

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

        await loadStandings();

        setupGroupFilter();

        setupSearchInput();

        setupNavigationEvents();

    } catch (error) {

        console.error("No se pudieron cargar los datos del dashboard:", error);

    }

}
/* ======================================================
   BUSCADOR
====================================================== */

// Lee el texto escrito por el usuario.
//
// HTML:
//
// <input id="team_search_input">
function getSearchText() {

    const searchInput = getElementById(
        "team_search_input"
    );

    if (!searchInput) {
        return "";
    }

    return searchInput.value;

}

function setSearchActive() {
    const searchInput = getElementById(
        "team_search_input"
    );

    if (!searchInput) {
        return;
    }

    searchInput.classList.add("search_active");
}

function removeSearchActive() {
    const searchInput = getElementById(
        "team_search_input"
    );

    if (!searchInput) {
        return;
    }

    searchInput.classList.remove("search_active");
}

/* ======================================================
    FILTRO DE EUIPOS
====================================================== */

// Filtra los equipos usando el texto
// escrito por el usuario.
async function filterStandings() {

    // Leemos el texto del buscador.
    const searchText = getSearchText()
        .trim()
        .toLowerCase();

    // Si está vacío,
    // mostramos todos los equipos.
    if (searchText === "") {

        removeSearchActive();

        await animateTableUpdate(function () {
            renderStandingsTable(
                standingsData
            );
        });

        return;

    }

    setSearchActive();

    // Array donde guardaremos
    // los equipos encontrados.
    const filteredTeams = [];

    // Recorremos todos los equipos.
    for (const team of standingsData) {

        // Convertimos el nombre del equipo
        // a minúsculas.
        const teamName = team.team
            .toLowerCase();

        // Si el nombre contiene el texto buscado...
        if (teamName.includes(searchText)) {

            filteredTeams.push(team);

        }

    }

    // Pintamos únicamente
    // los equipos encontrados.
    await animateTableUpdate(function () {
        renderStandingsTable(
            filteredTeams
        );
    });

}
/* ======================================================
    BUSCADOR EVENTOS
====================================================== */

// Activa el buscador.
//
// HTML:
//
// <input id="team_search_input">
function setupSearchInput() {

    const searchInput = getElementById(
        "team_search_input"
    );

    if (!searchInput) {
        return;
    }

    searchInput.addEventListener(
        "input",
        filterStandings
    );

}

/* ======================================================
    UX NAVIGATION
====================================================== */

// Devuelve el boton principal del sidebar segun la vista.
function getButtonByView(viewName) {

    if (viewName === "dashboard") {
        return getElementById("nav_dashboard_button");
    }

    if (viewName === "statistics") {
        return getElementById("nav_statistics_button");
    }

    if (viewName === "standings") {
        return getElementById("nav_standings_button");
    }

    return null;

}


// Devuelve la seccion HTML segun la vista.
function getSectionByView(viewName) {

    if (viewName === "dashboard") {
        return getElementById("hero_banner_container");
    }

    if (viewName === "statistics") {
        return getElementById("statistics_section_container");
    }

    if (viewName === "standings") {
        return getElementById("standings_section_container");
    }

    return null;

}


// Quita active de todos los botones del sidebar.
function clearActiveNavigation() {

    const navigationButtons = [
        getElementById("nav_dashboard_button"),
        getElementById("nav_statistics_button"),
        getElementById("nav_standings_button"),
    ];

    for (const button of navigationButtons) {

        if (button) {
            button.classList.remove("active");
        }

    }

}


// Activa el boton del sidebar correspondiente a la vista actual.
function setActiveNavigation(viewName) {

    clearActiveNavigation();

    const activeButton = getButtonByView(viewName);

    if (!activeButton) {
        return;
    }

    activeButton.classList.add("active");

}


// Aplica un glow temporal a la seccion visitada.
function focusSection(section) {

    if (!section) {
        return;
    }

    section.classList.remove("section_focus");

    window.setTimeout(
        function () {
            section.classList.add("section_focus");
        },
        0
    );

    window.setTimeout(
        function () {
            section.classList.remove("section_focus");
        },
        1300
    );

}


// Hace scroll hacia la seccion y actualiza la navegacion.
function navigateToSection(viewName) {

    const section = getSectionByView(viewName);

    if (!section) {
        return;
    }

    section.scrollIntoView({
        behavior: "smooth",
        block: "start",
    });

    setActiveNavigation(viewName);
    focusSection(section);

}


// Conecta botones del sidebar y del hero con sus secciones.
function setupNavigationEvents() {

    const dashboardButton = getElementById("nav_dashboard_button");
    const statisticsButton = getElementById("nav_statistics_button");
    const standingsButton = getElementById("nav_standings_button");
    const heroStatisticsButton = getElementById("hero_statistics_button");
    const heroStandingsButton = getElementById("hero_standings_button");

    if (dashboardButton) {
        dashboardButton.addEventListener(
            "click",
            function () {
                navigateToSection("dashboard");
            }
        );
    }

    if (statisticsButton) {
        statisticsButton.addEventListener(
            "click",
            function () {
                navigateToSection("statistics");
            }
        );
    }

    if (standingsButton) {
        standingsButton.addEventListener(
            "click",
            function () {
                navigateToSection("standings");
            }
        );
    }

    if (heroStatisticsButton) {
        heroStatisticsButton.addEventListener(
            "click",
            function () {
                navigateToSection("statistics");
            }
        );
    }

    if (heroStandingsButton) {
        heroStandingsButton.addEventListener(
            "click",
            function () {
                navigateToSection("standings");
            }
        );
    }

}

// Espera a que el HTML exista antes de buscar IDs.
document.addEventListener(
    "DOMContentLoaded",
    initializeDashboard
)
