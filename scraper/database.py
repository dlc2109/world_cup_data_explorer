import sqlite3
import json

DATABASE_PATH = "data/world_cup.db"


def create_connection():
    try:
        connection = sqlite3.connect(DATABASE_PATH)
        return connection
    except sqlite3.Error as error:
        print(f"Error al conectar con la base de datos: {error}")
        return None


def create_standings_table():
    connection = create_connection()

    if connection is None:
        print("No se pudo crear la tabla porque no hay conexión.")
        return

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS standings (
                group_name TEXT,
                position INTEGER,
                team TEXT,
                played INTEGER,
                wins INTEGER,
                draws INTEGER,
                losses INTEGER,
                goals_for INTEGER,
                goals_against INTEGER,
                goal_difference INTEGER,
                points INTEGER,
                qualification TEXT,
                source_url TEXT,
                updated_at TEXT
            )
            """
        )

        connection.commit()
        print("Tabla standings creada correctamente.")

    except sqlite3.Error as error:
        print(f"Error al crear la tabla standings: {error}")

    finally:
        connection.close()


def load_standings_from_json(json_path="data/standings.json"):
    try:
        with open(json_path, "r", encoding="utf-8") as json_file:
            records = json.load(json_file)

        return records

    except FileNotFoundError:
        print(f"No se encontró el archivo JSON: {json_path}")
        return []

    except json.JSONDecodeError as error:
        print(f"Error leyendo el JSON: {error}")
        return []


# creamos una funcion para insertar registros en SQLite.
# Esta funcion recibe la lista de diccionarios leida desde standings.json.
def insert_standings(records):
    connection = None

    try:
        connection = create_connection()

        if connection is None:
            print("No se pudo abrir la conexión con SQLite.")
            return

        cursor = connection.cursor()

        cursor.execute("DELETE FROM standings")

        insert_query = """
            INSERT INTO standings (
                group_name,
                position,
                team,
                played,
                wins,
                draws,
                losses,
                goals_for,
                goals_against,
                goal_difference,
                points,
                qualification,
                source_url,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        for record in records:
            cursor.execute(
                insert_query,
                (
                    record["group_name"],
                    record["position"],
                    record["team"],
                    record["played"],
                    record["wins"],
                    record["draws"],
                    record["losses"],
                    record["goals_for"],
                    record["goals_against"],
                    record["goal_difference"],
                    record["points"],
                    record.get("qualification", ""),
                    record["source_url"],
                    record["updated_at"],
                ),
            )

        connection.commit()
        print(f"Registros insertados: {len(records)}")

    except sqlite3.Error as error:
        print(f"Error insertando registros en SQLite: {error}")

    except KeyError as error:
        print(f"Falta una clave en el registro JSON: {error}")

    finally:
        if connection is not None:
            connection.close()

def count_standings():
    connection=None
    try:
        connection=create_connection()
        if connection is None:
            return 0
        cursor=connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM STANDINGS")
        result = cursor.fetchone()
        return result[0]
    except sqlite3.Error as error:
        print(f"Error contando registros: {error}")
        return 0

    finally:
        if connection is None:
            connection.close()

#muestra todos
def get_all_standings():
    connection=None
    try:
        connection=create_connection()
        if connection is None:
             return []
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM standings")
        records = cursor.fetchall()
        return records
    except sqlite3.Error as error:
        print(f"Error consultando standings: {error}")
        return []

    finally:
       
        if connection is not None:
            connection.close()


#
def get_standings_by_group(group_name):
    connection = None

    try:
        #  limpiamos el valor recibido.
        group_name = str(group_name).strip().upper()

        connection = create_connection()

        if connection is None:
            return []
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM standings WHERE group_name = ?",
            (group_name,)
        )
        records = cursor.fetchall()
        return records

    except sqlite3.Error as error:
        print(f"Error consultando el grupo {group_name}: {error}")
        return []

    finally:
        if connection is not None:
            connection.close()

if __name__ == "__main__":
    total = count_standings()
    print("Total de registros:", total)

    all_records = get_all_standings()
    print("Primeros registros:", all_records[:3])

    group_d = get_standings_by_group("D")
    print("Registros del Grupo D:", group_d)