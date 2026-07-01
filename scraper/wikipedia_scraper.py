import requests

URL = "https://en.wikipedia.org/wiki/2026_FIFA_World_Cup_Group_D"

HEADERS = {"User-Agent": "CoderHubEducationalProject/1.0"}



def download_group_d_page():
    group_d_url = "https://en.wikipedia.org/wiki/2026_FIFA_World_Cup_Group_D"
    response = requests.get(URL, headers=HEADERS,timeout =20)       
    print ("estado:", response.status_code)
    print("tamano HTML:" , len(response.text) )

    response.raise_for_status()

    return response.text

if __name__ == "__main__":
    html = download_group_d_page()
    print("Descarga html completada.")    
