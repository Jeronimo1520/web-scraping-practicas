import requests
import pandas as pd

"""
- Extraer nombre, reviews y rating de los cursos de Python.
    - Aprender a extraer datos de APIs.
    - Aprender a investigar y decifrar la forma en que una pagina web que carga sus datos por API.
    - Aprender a hacer requerimientos a un API del cual no tenemos documentacion.
    - Aprender a utilizar la consola de NETWORKS de Google Chrome.
    - Aprender a procesar datos en formato JSON.
    
"""
headers = {
    # El encabezado de referer es importante. Sin esto, este API en especifico me respondera 403
    "Referer": "https://www.udemy.com/courses/search/?src=ukw&q=python",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/119.0.0.0 Safari/537.36"
}
for i in range(1,4):
    url_api = 'https://www.udemy.com/api-2.0/search-courses/?src=ukw&q=python&skip_price=true&p=' + str(i)
    response = requests.get(url_api, headers=headers)
    print(response.json())

    data = response.json()

    cursos = data["courses"]

    for curso in cursos:
        print(curso["title"])
        print(curso["num_reviews"])
        print(curso["rating"])
        print()
