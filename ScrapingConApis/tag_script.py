import requests
from lxml import html
import json

headers = {
    "user-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/119.0.0.0 Safari/537.36'
}
for i in range(1,3):
    url = "https://www.gob.pe/busquedas?contenido[]=normas&institucion[]=mininter&sheet=" + str(i) + "&sort_by_=recent"
    respuesta = requests.get(url, headers=headers)
    respuesta.encoding = 'UTF-8'
    parser = html.fromstring(respuesta.text)

    datos = parser.xpath('//script[contains(text(),"window.initialData")]')[0].text_content()

    indice_inicial = datos.find('{')

    datos = datos[indice_inicial:]

    objeto = json.loads(datos)

    resultados = objeto["data"]["attributes"]["results"]

    for resultado in resultados:
        if resultado:
            print(resultado["content"])