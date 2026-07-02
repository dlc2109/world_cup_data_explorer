# convertir la tabla HTML a DataFrame;
# después limpiar nombres de columnas;
# después acomodar valores;
# después preparar los datos para guardarlos o reutilizarlos.

from  io import StringIO #convierte un texto normal en un objeto parecido a un archivo en memoria.(BUFFER)
import pandas as pd #librería para el manejo de datos.
import re # estto es para eliminar  cosas raras entre parentesis 


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
def clean_standing_dataframe(df): 
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

if __name__ == "__main__":
    from wikipedia_scraper import download_group_d_page
    from parsers import find_standings_table

    html = download_group_d_page()
    standings_table = find_standings_table(html)

    df = convert_html_to_dataframe(standings_table)
    df = clean_standing_dataframe(df)
    df = clean_standings_values(df)

    print("\n=== DataFrame limpio ===")
    print(df.head())

    print("\nTipos de datos:")
    print(df.dtypes)
