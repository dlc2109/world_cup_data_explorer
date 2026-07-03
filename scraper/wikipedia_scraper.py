import requests

# Grupos válidos del Mundial.
GROUPS = "ABCDEFGHIJKL"

# URL base para construir la página de cualquier grupo.
BASE_URL = "https://en.wikipedia.org/wiki/2026_FIFA_World_Cup_Group_{}"

# Headers de la solicitud.
HEADERS = {
    "User-Agent": "CoderHubEducationalProject/1.0"
}

# Tiempo máximo de espera.
TIMEOUT = 20


# Función general para descargar cualquier grupo.
def download_group_page(group_letter):
    # Convertimos la letra recibida a texto,
    # quitamos espacios y la pasamos a mayúsculas.
    group_letter = str(group_letter).strip().upper()

    # Validamos que el grupo exista.
    if group_letter not in GROUPS:
        raise ValueError(f"Grupo inválido: {group_letter}")

    # Construimos la URL del grupo.
    url = BASE_URL.format(group_letter)

    try:
        # Descargamos la página.
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=TIMEOUT
        )

        print("estado:", response.status_code)
        print("tamano HTML:", len(response.text))

        # Lanza una excepción si hubo un error HTTP.
        response.raise_for_status()

        # Devolvemos el HTML.
        return response.text

    except requests.exceptions.Timeout:
        print("Error: la solicitud tardó demasiado.")
        return None

    except requests.exceptions.HTTPError as error:
        print(f"Error HTTP: {error}")
        return None

    except requests.exceptions.RequestException as error:
        print(f"Error al conectar con Wikipedia: {error}")
        return None


# Función de la  prueba del Grupo D.
def download_group_d_page():
    return download_group_page("D")




# Prueba 
if __name__ == "__main__":
    html = download_group_d_page()

    if html is not None:
        print("Descarga HTML completada.")