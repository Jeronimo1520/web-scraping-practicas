import requests
from bs4 import BeautifulSoup

url_semilla = 'https://file-examples.com/index.php/sample-documents-download/sample-xls-download/'

headers = {
    "user-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/119.0.0.0 Safari/537.36'
}
response = requests.get(url_semilla, headers=headers)

# Creamos la sopa para poder parsear el contenido de la web en formato texto
soup = BeautifulSoup(response.text, features="lxml")#Este uso es para el warning lxml

urls_archivos = [] #URLs de los archivos que encuentre

descargas = soup.find_all('a', class_="download-button")

# Iteramos la lista de resultados para conseguir la url de cada una de ellas.
for descarga in descargas:
    # Esta es la forma de conseguir el valor de un atributo con BeautifulSoup
    urls_archivos.append(descarga['href'])

print(urls_archivos)

for url in urls_archivos:
    # Hace un requests a cada url permitiendo las redirecciones por si el archivo
    # estuviera fuera del ámbito de la página actual.

    # Parece que la url del archivo se cambia, por lo que a la hora de bajar el
    # archivo, no funciona. Hay que reemplazar la url final igual que lo hace la
    # propia página web.

    url = url.replace("wp-content/storage/", "storage/fee4254a29658d857963fcd/")

    # Con la url modificada ya podemos hacer el requerimiento al archivo
    response = requests.get(url, allow_redirects=True)
    file_name = './archivos/' + (url.split("/")[-1])

    # Abrimos un archivo en nuestro hd para poder volcar la captura del archivo web
    # usando su mismo nombre capturado en el paso anterior.
    output = open(file_name, 'wb')

    # Escribimos en el archivo de nuestro hd, el "contenido" de la extracción del
    # requests al archivo de la web.
    output.write(response.content)

    # cerramos el archivo del hd ya lleno con los datos.
    output.close()






