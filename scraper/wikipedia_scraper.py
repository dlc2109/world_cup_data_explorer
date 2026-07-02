import requests

URL = "https://en.wikipedia.org/wiki/2026_FIFA_World_Cup_Group_D"
HEADERS = {"User-Agent": "CoderHubEducationalProject/1.0"}
TIMEOUT = 20


def download_group_d_page():
    try:
        response = requests.get(URL, headers=HEADERS, timeout=TIMEOUT)

        print("estado:", response.status_code)
        print("tamano HTML:", len(response.text))

        response.raise_for_status()

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