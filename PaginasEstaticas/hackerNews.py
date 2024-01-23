import requests
from bs4 import BeautifulSoup

url = "https://news.ycombinator.com"

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu "
                  "Chromium/115.0.0.0 Safari/537.36"
}
response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")

listado_noticias = soup.find_all('tr', class_='athing')

for noticia in listado_noticias:
    titulo = noticia.find('span', class_='titleline').text

    url = noticia.find('span', class_='titleline').find('a').get('href')

    metadata = noticia.find_next_sibling()

    score = 0
    comentarios = 0

    try:
        score_tmp = metadata.find('span', class_='score').text
        score = int(score_tmp.strip().replace('points', ''))
    except:
        print('Score no disponible')

    try:
        comentarios_tmp = metadata.find('span', attrs={'class': 'subline'}).text
        comentarios_tmp = comentarios_tmp.split("|")[-1]
        comentarios = int(comentarios_tmp.strip().replace('comments', ''))
    except:
        print('Comentarios no disponibles')


    print(titulo)
    print(url)
    print(score)
    print(comentarios)
    print()
