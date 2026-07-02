from bs4 import BeautifulSoup


#--------------------------------------------------------------------------#
# 1. encontrar la sección correcta;
# 2. ubicar la tabla correcta;
# 3. validar que esa tabla parece ser la de posiciones.
# -------------------------------------------------------------------------#


def find_standings_table(html):
    # Creamos el objeto BeautifulSoup para poder recorrer el HTML.
    soup = BeautifulSoup(html, "html.parser")

    # Buscamos la sección "Standings".
    heading = soup.find("h2", id="Standings")

    # Si no existe la sección, detenemos el programa.
    if heading is None:
        raise ValueError("No se encontró la sección Standings")

    # Variable donde guardaremos la tabla cuando la encontremos.
    standings_table = None

    # Recorremos todos los elementos que vienen después de "Standings".
    # Solo nos interesan etiquetas <h2> y <table>.
    for element in heading.find_all_next(["h2", "table"]):

        # Si aparece otro <h2>, significa que salimos de la sección Standings.
        if element.name == "h2":
            break

        # Si encontramos una tabla, revisamos si es la correcta.
        if element.name == "table":

            # Obtenemos todos los encabezados de la tabla.
            headers = " ".join(
                th.get_text(" ", strip=True)
                for th in element.find_all("th")
            )

            # Encabezados obligatorios 
            required = ["Team", "Pld", "GF", "GA", "GD", "Pts"]

            # Comprobamos que todos los encabezados existan.
            if all(name in headers for name in required):
                standings_table = element
                break

    # Si no encontramos una tabla válida, lanzamos un error.
    if standings_table is None:
        raise ValueError("No se encontró una tabla de posiciones válida")

    # Devolvemos la tabla encontrada.
    return standings_table

if __name__ == "__main__":
           from wikipedia_scraper import download_group_d_page
           html = download_group_d_page()
           table = find_standings_table(html)
           print("!!!tabla  de pocisiones encontrada exitosamenre!!!")