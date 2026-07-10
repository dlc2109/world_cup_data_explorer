
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

@app.route('/api/standings', methods=['GET'])
def get_standings():
    #1 Obtener todos los datos 
    data = get_all_standings()
    data_dicts = [dict(row) for row in data] #(convertimos los objetivos sqlite3.Row a diccionarios estandar (dictionary))
    
   
    filter_type = request.args.get('filter') # obtenr los valores de los parametrosClasificados
    

    # Si piden clasificados
    if filter_type == 'qualified':
        # en caso de que la posición sea 1° o 2°, aunque debería incluir los 3°
        teams_qualified = (list(filter(lambda t: t['position'] <= 3, data_dicts)))

        #list filter ambda es una función anónima
        # -- Lambda t: es el argumento, es como decirle "toma un elemento de la colección"
        #" t['position ]" es la condición
        # otra opciónes una list comprehension

       # qualified = [t for t in data_dicts if t['Position'] <= 3]

        return jsonify(teams_qualified)
    
    
    
    # Si no piden nada, regresamos todo
    return jsonify(data_dicts)

if __name__ == "__main__":
    app.run(debug=True)