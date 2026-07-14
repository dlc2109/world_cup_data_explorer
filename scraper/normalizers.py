

from  io import StringIO #convierte un texto normal en un objeto parecido a un archivo en memoria.(BUFFER)
import pandas as pd #librería para el manejo de datos.
import re # estto es para eliminar  cosas raras entre parentesis 
from datetime import datetime
from scraper.wikipedia_scraper import download_group_page, BASE_URL, GROUPS
from scraper.parsers import find_standings_table

# convertir la tabla HTML a DataFrame;
# después limpiar nombres de columnas;
# después acomodar valores;
# después preparar los datos para guardarlos o reutilizarlos.

# 1.funcion para convertir tabla  html a dataframe

def convert_html_to_dataframe(standings_table):
    table_html = str(standings_table) #Convertimos esa tabla de BeautifulSoup a texto HTML.
    buffer = StringIO(table_html) # buffer cambia la forma en que lo recibe
    frames=pd.read_html(buffer)#pandas lee el archivo de buffer

    df=frames[0] #primera tabla encontrada
    print(df.columns) #imrimimos los nombres de las columnas+
    print(df.head()) # muestra las primeras filas
    return df # retorna el Dataframe



#2ya teneiendo el DAtaframe vamos a limiarlo ( EJ : Teamvte → team)
 # recibimos el  dataframe = df  como parametro 
def clean_standings_dataframe(df): 
    df.columns=df.columns.str.strip()#limpia los espacios
    column_mapping ={ #creamos el diccionario con los nombres claros
    "Pos": "position",
        "Teamvte": "team",
        "Pld": "played",
        "W": "wins",
        "D": "draws",
        "L": "losses",
        "GF": "goals_for",
        "GA": "goals_against",
        "GD": "goal_difference",
        "Pts": "points",
        "Qualification": "qualification",
    }
  
# Pandas revisa cada columna y, si aparece en el diccionario, la cambia por su nuevo nombre.
    df =df.rename(columns=column_mapping)
    return df  # retornoams el df con sus nombres nuevos

    

#funcion para limpiar los nombres de equipos como united states (h)
#re sub es para sustituir 
def clean_team_name(team_name):
    team_name =str(team_name)
    team_name = re.sub(r"\s*\([^)]*\)\s*$", "", team_name)
    team_name =team_name.strip()
    return team_name


# creamos una funcion pequena para limpiar puntos.
# Esta funcion quitara notas entre corchetes, por ejemplo "4[a]" -> "4".

def clean_points(points_value):
    points_value=str(points_value)
    points_value=re.sub(r"\[[^\]]*\]", "", points_value)
    points_value = points_value.strip()
    return int(points_value)

#  creamos una funcion pequena para limpiar goal_difference.
# Esta funcion cambia el simbolo Unicode de menos por el signo normal
# y luego convierte el valor a entero.   

def clean_goal_difference(goal_difference_value):
    goal_difference_value=str(goal_difference_value)
    goal_difference_value = goal_difference_value.replace("−", "-")
    goal_difference_value =goal_difference_value.strip()
    return int(goal_difference_value)

# creamos una funcion para convertir columnas numericas.
# Esta funcion aplicara conversion a entero en las columnas numericas del DataFrame.
def convert_numeric_columns(df): #pasamos eel dataframe completo
    numeric_columns = [  #lista de columnas
        "position",
        "played",
        "wins",
        "draws",
        "losses",
        "goals_for",
        "goals_against",
        "goal_difference",
        "points",
    ]
    
    for column in numeric_columns: # la iteranos
        df[column]=df[column].astype(int) #astype() es un método de pandas.
# Sirve para cambiar el tipo de dato de una columna.
    return df 

def clean_standings_values(df):    
    df["team"] = df["team"].apply(clean_team_name)
    df["points"] = df["points"].apply(clean_points)
    df["goal_difference"] = df["goal_difference"].apply(clean_goal_difference)
    df = convert_numeric_columns(df)
    return df


#GUARDAR EN JSON LOS DATOS LIMPIOS
#funcion dos parametros el dataframe y output_path  que es la ruta donde vamos a guardar momentaneamente
# Paso 44: usamos to_json de pandas.
    # orient="records" guarda una lista de objetos JSON.
    # force_ascii=False conserva caracteres especiales correctamente.
    # indent=2 deja el archivo bien formateado y facil de leer.

def save_dataframe_to_json(df, output_path):
    df.to_json( output_path,
    orient="records",
    force_ascii=False,
    indent=2)
# agregamos columnas nuevas de source y update
def add_metadata(df,group_name,source_url):
    df["group_name"] =group_name
    df["source_url"] = source_url
    df["updated_at"]=datetime.now().isoformat()
    return df

## def process_group(group_letter): Procesa un grupo completo: descarga el HTML, encuentra la tabla,
# limpia los datos, agrega metadata y guarda el JSON final.
def process_group(group_letter):
    group_letter = str(group_letter).strip().upper()

    html = download_group_page(group_letter)

    if html is None:
        print(f"No se pudo descargar el Grupo {group_letter}.")
        return None

    standings_table = find_standings_table(html)

    df = convert_html_to_dataframe(standings_table)

    df = clean_standings_dataframe(df)

    df = clean_standings_values(df)

    source_url = BASE_URL.format(group_letter)

    df = add_metadata(
        df,
        group_name=group_letter,
        source_url=source_url
    )

    output_path = f"data/group_{group_letter.lower()}_standings.json"

    save_dataframe_to_json(df, output_path)

    print(f"Grupo {group_letter} guardado en {output_path}")

    return df

# def process_all_groups (): Recorre todos los grupos definidos en GROUPS,
# procesa cada uno y continúa aunque alguno falle.
def process_all_groups ():
  processed_groups = []
  for group in  GROUPS:
    try:
        process_group(group)
        processed_groups.append(group)
        print(f"Grupo {group} procesado correctamente.")
    except Exception as error:
        print(f"Error procesando el grupo {group}: {error}")

  return processed_groups

# Esta funcion recorrera todos los grupos definidos en GROUPS,
# procesara cada uno con process_group(group)
# y unira todos los resultados en un solo DataFrame.
def process_all_groups_to_dataframe():
    all_dataframes = []
    for group in GROUPS:
        try:
            df = process_group(group)
            if df is not None:
             all_dataframes.append(df)
             print(f"Grupo {group} agregado al DataFrame final.")
        except Exception as error:
            print(f"Error procesando el grupo {group}: {error}")
    if not all_dataframes:
         raise ValueError("No se pudo procesar ningun grupo correctamente.")
          #combinamos todos los DataFrames en uno solo.
          # pandas.concat() une todos los DataFrames de la lista.   
    combined_df = pd.concat(all_dataframes, ignore_index=True)
    return combined_df



if __name__ == "__main__":
    df = process_all_groups_to_dataframe()

    save_dataframe_to_json(df, "data/standings.json")

    print("\nDataFrame combinado:")
    print(df.head())

    print("\nTotal de registros:")
    print(len(df))

    print("JSON consolidado guardado en data/standings.json")
