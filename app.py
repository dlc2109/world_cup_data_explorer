from flask import Flask, jsonify, request,render_template
from scraper.database import (
    get_all_standings,
    get_standings_by_group,
    create_standings_table,
    load_standings_from_json,
    insert_standings,
    count_standings,
)
from scraper.normalizers import (
    process_all_groups_to_dataframe,
    save_dataframe_to_json
)

from services.statistics_service import get_dashboard_statistics


app = Flask(__name__)
STANDINGS_COLUMNS = [
    "group_name",
    "position",
    "team",
    "played",
    "wins",
    "draws",
    "losses",
    "goals_for",
    "goals_against",
    "goal_difference",
    "points",
    "qualification",
    "source_url",
    "updated_at",
]


def row_to_dict(row):
    return dict(zip(STANDINGS_COLUMNS, row))

#ruta principal.
@app.route("/")
def home():
    return render_template("index.html")

# Esta def statistics()  ruta devuelve una estadística sencilla
# para comprobar que Flask puede consultar SQLite.
@app.route("/api/statistics")

def statistics():
    dashboard_statistics = get_dashboard_statistics()

    return jsonify(dashboard_statistics)



# Esta ruta devuelve todos los standings o filtra por grupo 
@app.route("/api/standings")
def standings():
    group = request.args.get("group")

    if group:
        rows = get_standings_by_group(group)
    else:
        rows = get_all_standings()

    standings_data = [
        row_to_dict(row)
        for row in rows
    ]

    return jsonify(standings_data)

# ======================================================
# REFRESH API
# ======================================================
# Esta ruta pertenece a Flask.
# Su responsabilidad sera actualizar los datos del proyecto.
# En este paso solo regeneramos data/standings.json.
# Todavia NO actualizamos SQLite.
@app.route("/api/refresh", methods=["POST"])
@app.route("/api/refresh", methods=["POST"])
def refresh_data():
    print("POST /api/refresh recibido", flush=True)

    try:
        print("Iniciando scraper...", flush=True)

        # process_all_groups_to_dataframe viene de scraper/normalizers.py.
        # Descarga todos los grupos, encuentra Standings,
        # limpia los datos y devuelve un DataFrame combinado.
        df = process_all_groups_to_dataframe()

        print("Scraper terminado", flush=True)
        print("Guardando data/standings.json...", flush=True)

        # save_dataframe_to_json viene de scraper/normalizers.py.
        # Guarda el DataFrame actualizado como JSON.
        save_dataframe_to_json(
            df,
            "data/standings.json"
        )

        print("JSON actualizado correctamente", flush=True)
        print("Actualizando SQLite...", flush=True)

        # create_standings_table viene de scraper/database.py.
        # Asegura que la tabla standings exista antes de insertar datos.
        create_standings_table()

        # load_standings_from_json viene de scraper/database.py.
        # Lee el JSON actualizado y devuelve una lista de diccionarios.
        records = load_standings_from_json("data/standings.json")

        # insert_standings viene de scraper/database.py.
        # Borra registros viejos e inserta los datos nuevos en SQLite.
        insert_standings(records)

        # count_standings viene de scraper/database.py.
        # Confirma cuantos registros quedaron guardados en SQLite.
        total_records = count_standings()

        print("SQLite actualizado correctamente", flush=True)

        # jsonify viene de Flask.
        # Devolvemos respuesta final al frontend.
        return jsonify({
            "status": "success",
            "message": "Datos actualizados correctamente",
            "total_records": total_records
        })

    except Exception as error:
        print(f"Error en /api/refresh: {error}", flush=True)

        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
