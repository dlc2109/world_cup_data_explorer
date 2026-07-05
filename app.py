from flask import Flask, jsonify, request,render_template
from scraper.database import (
    get_all_standings,
    get_standings_by_group,
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


if __name__ == "__main__":
    app.run(debug=True)