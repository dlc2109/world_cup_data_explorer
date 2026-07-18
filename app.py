from flask import Flask, jsonify, request, render_template
from scraper.database import *
import json
import sqlite3
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

#en este punto cree una ruta de conexión a la database, en lugar de tener que ejecutarla 10mil veces, creo una función y llamo a esa funcion loloddkdokdokdod
def query_db(query, args=(), one = False):
    conn = sqlite3.connect('data/world_cup.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, args) #voy a ser honesto me dió flojera nombrar el cursor
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv #funciones de una sola linea

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
    filter_type = request.args.get('filter') # obtenr los valores de los parametrosClasificados
    team = request.args.get('team', '').strip()
    action = request.args.get('action')

    # --- FUNCIÓN DE BÚSQUEDA AÑADIDA AL MANEJADOR PRINCIPAL ---
    if team:
        try:
            standing_row = query_db("SELECT * FROM standings WHERE team LIKE ?", (f"%{team}%",), one = True)
            match_rows = query_db("""
                SELECT * FROM partidos_eliminacion
                WHERE local_team LIKE ? OR away_team LIKE ?        
            """, (f"%{team}%", f"%{team}%"))
            result = {
                "standing": dict(standing_row) if standing_row else None,
                "knockout_matches": [dict(row) for row in match_rows] if match_rows else []
            }
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # --- FUNCIÓN DEL TOP GOLES DESDE TU ARCHIVO JSON ---
    if action == 'top_goles' or filter_type == 'top_goles':
        try:
            with open('static/knockout.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            # reverse=True para que vayan de mayor a menor cantidad de goles
            data_ordenada = sorted(data, key=lambda x: x.get('local_goals', 0) + x.get('away_goals', 0), reverse=True)
            return jsonify(data_ordenada)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Lógica estándar de grupos o clasificados que ya tenías
    if group:
        rows = get_standings_by_group(group)
        standings_data = [row_to_dict(row) for row in rows]
        return jsonify(standings_data)

    data = get_all_standings()
    data_dicts = [dict(row) for row in data] #(convertimos los objetivos sqlite3.Row a diccionarios estandar (dictionary))

    # Si piden clasificados
    if filter_type == 'qualified':
        # en caso de que la posición sea 1° o 2°, aunque debería incluir los 3°
        teams_qualified = (list(filter(lambda t: t.get('position', 0) <= 3, data_dicts)))
        #list filter ambda es una función anónima
        # -- Lambda t: es el argumento, es como decirle "toma un elemento de la colección"
        #" t['position ]" es la condición
        # otra opciónes una list comprehension
        # qualified = [t for t in data_dicts if t['Position'] <= 3]
        return jsonify(teams_qualified)
    
    # Si no piden nada, regresamos todo
    return jsonify(data_dicts)

@app.route('/api/knockout')
def get_knouckout_results():
    try:
        rows = query_db("""
        SELECT id, ko_round, local_team, away_team, local_goals, away_goals, penalties, state, updated_at
        FROM partidos_eliminacion
        ORDER BY id ASC
""")
        partidos = [dict(row) for row in rows]
        return jsonify(partidos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/search_team', methods=['GET'])
def search_team():
    team = request.args.get('team', '').strip()
    if not team:
        return jsonify({"error": "No team specified"}), 400

    try:
       
        standing_row = query_db("SELECT * FROM standings WHERE team LIKE ?", (f"%{team}%",), one = True)
        
        match_rows = query_db("""
            SELECT * FROM partidos_eliminacion
            WHERE local_team LIKE ? OR away_team LIKE ?        
        """, (f"%{team}%", f"%{team}%"))
        
        
        result = {
            "standing": dict(standing_row) if standing_row else None,
            "knockout_matches": [dict(row) for row in match_rows] if match_rows else []
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/top_goles', methods=['GET'])
def get_top_goles():
    try:
        # Abrimos el archivo JSON de la carpeta static
        with open('static/knockout.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        # reverse=True para que vayan de mayor a menor cantidad de goles totales
        # Usamos .get() por seguridad si algún partido no tiene goles cargados aún
        data_ordenada = sorted(data, key=lambda x: x.get('local_goals', 0) + x.get('away_goals', 0), reverse=True)
        
        return jsonify(data_ordenada)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)