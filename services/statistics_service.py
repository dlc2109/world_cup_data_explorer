
# ======================================================
# STATISTICS SERVICE
# ======================================================
# Este archivo calcula las estadísticas que se mostrarán
# en las cards del dashboard.
#
# Contexto:
# app.py recibe la peticion del navegador.
# database.py consulta los datos guardados en SQLite.
# statistics_service.py calcula los indicadores que usa /api/statistics.
#
# app.py usará este servicio para responder:
#
# GET /api/statistics
#  importamos las funciones de consulta desde database.py.
from scraper.database import get_all_standings


# TEAM_INDEX: posicion del nombre del equipo dentro de la tupla de SQLite.
TEAM_INDEX = 2

# PLAYED_INDEX: posicion de partidos jugados dentro de la tupla de SQLite.
PLAYED_INDEX = 3

# GOALS_FOR_INDEX: posicion de goles a favor dentro de la tupla de SQLite.
GOALS_FOR_INDEX = 7

# GOALS_AGAINST_INDEX: posicion de goles en contra dentro de la tupla de SQLite.
GOALS_AGAINST_INDEX = 8

# UPDATED_AT_INDEX: posicion de la fecha de actualizacion dentro de la tupla.
UPDATED_AT_INDEX = 13


# get_standings_data: obtiene todos los registros guardados en SQLite.
def get_standings_data():
    standings = get_all_standings()
    return standings


# get_total_matches: calcula el total de partidos jugados.
def get_total_matches(standings):
    total_played = 0

    for team in standings:
        total_played += team[PLAYED_INDEX]

    return total_played // 2


# get_total_goals: suma todos los goles anotados por los equipos.
def get_total_goals(standings):
    total_goals = 0

    for team in standings:
        total_goals += team[GOALS_FOR_INDEX]

    return total_goals


# get_average_goals: calcula el promedio de goles por partido.
def get_average_goals(total_goals, total_matches):
    if total_matches == 0:
        return 0

    return round(total_goals / total_matches, 2)


# get_best_offense: busca el equipo con mas goles a favor.
def get_best_offense(standings):
    best_team = None

    for team in standings:
        if best_team is None:
            best_team = team
        elif team[GOALS_FOR_INDEX] > best_team[GOALS_FOR_INDEX]:
            best_team = team

    return best_team


# get_best_defense: busca el equipo con menos goles en contra.
def get_best_defense(standings):
    best_team = None

    for team in standings:
        if best_team is None:
            best_team = team
        elif team[GOALS_AGAINST_INDEX] < best_team[GOALS_AGAINST_INDEX]:
            best_team = team

    return best_team


# get_last_update: toma la fecha de ultima actualizacion de los datos.
def get_last_update(standings):
    if not standings:
        return None

    return standings[0][UPDATED_AT_INDEX]


# get_dashboard_statistics: arma el diccionario final para /api/statistics.
def get_dashboard_statistics():
    standings = get_standings_data()

    total_matches = get_total_matches(standings)
    total_goals = get_total_goals(standings)
    average_goals = get_average_goals(total_goals, total_matches)
    best_offense = get_best_offense(standings)
    best_defense = get_best_defense(standings)
    updated_at = get_last_update(standings)

    statistics = {
        "total_records": len(standings),
        "total_matches": total_matches,
        "total_goals": total_goals,
        "average_goals": average_goals,
        "best_offense_team": best_offense[TEAM_INDEX],
        "best_offense_goals": best_offense[GOALS_FOR_INDEX],
        "best_defense_team": best_defense[TEAM_INDEX],
        "best_defense_goals": best_defense[GOALS_AGAINST_INDEX],
        "updated_at": updated_at,
    }

    return statistics


# get_total_matches: calcula partidos totales usando los partidos jugados.
def get_total_matches(standings):
    total_played = 0

    for team in standings:
        total_played += team[PLAYED_INDEX]

    total_matches = total_played // 2

    return total_matches


# get_total_goals: suma los goles a favor de todos los equipos.
def get_total_goals(standings):
    total_goals = 0

    for team in standings:
        total_goals += team[GOALS_FOR_INDEX]

    return total_goals


# get_average_goals: calcula el promedio de goles por partido.
def get_average_goals(total_goals, total_matches):

    if total_matches == 0:
        return 0

    average_goals = total_goals / total_matches

    return round(average_goals, 2)


# get_best_offense: busca el equipo con mas goles a favor.
def get_best_offense(standings):
    best_team = None

    for team in standings:

        if best_team is None:
            best_team = team

        elif team[GOALS_FOR_INDEX] > best_team[GOALS_FOR_INDEX]:
            best_team = team

    return best_team


# get_best_defense: busca el equipo con menos goles en contra.
def get_best_defense(standings):
    best_team = None

    for team in standings:

        if best_team is None:
            best_team = team

        elif team[GOALS_AGAINST_INDEX] < best_team[GOALS_AGAINST_INDEX]:
            best_team = team

    return best_team


# get_last_update: devuelve la fecha de actualizacion del primer registro.
def get_last_update(standings):

    if not standings:
        return None

    return standings[0][UPDATED_AT_INDEX]


# get_dashboard_statistics: arma el diccionario final para la API.
def get_dashboard_statistics():
    standings = get_standings_data()

    total_matches = get_total_matches(standings)
    total_goals = get_total_goals(standings)
    average_goals = get_average_goals(total_goals, total_matches)

    best_offense = get_best_offense(standings)
    best_defense = get_best_defense(standings)

    updated_at = get_last_update(standings)

    statistics = {
        "total_records": len(standings),
        "total_matches": total_matches,
        "total_goals": total_goals,
        "average_goals": average_goals,
        "best_offense_team": best_offense[TEAM_INDEX],
        "best_offense_goals": best_offense[GOALS_FOR_INDEX],
        "best_defense_team": best_defense[TEAM_INDEX],
        "best_defense_goals": best_defense[GOALS_AGAINST_INDEX],
        "updated_at": updated_at,
    }

    return statistics