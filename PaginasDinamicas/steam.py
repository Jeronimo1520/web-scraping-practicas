import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time

url = 'https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&tags=19&infinite=1'

def get_data(url):
    r = requests.get(url)
    #convertir json a dict de python
    data = dict(r.json())
    return data['results_html']

def parse_games(data):
    games_list = []
    soup = BeautifulSoup(data, 'html.parser')
    games = soup.find_all('a')
    for game in games:
        title = game.find('span', class_='title').text
        try:
            price = game.find('div', class_ = 'discount_final_price').text.strip().split('COL')
        except:
            price = 'N/A'
        try:
           discount_original_price = game.find('div', class_='discount_original_price').text.strip()
        except:
            discount_original_price = 'N/A'
        try:
            discount = game.find('div', class_='discount_pct').text.strip()
        except:
            discount = 'N/A'

        game_info = {
            'Title': title,
            'Price': price,
            'Original price': discount_original_price,
            'Discount': discount
        }
        games_list.append(game_info)

    return games_list
def totalresults(url): #Adquiere la cadntidad total de juegos que se encuentra en el JSON obtenido en la URL
    r = requests.get(url)
    data = dict(r.json())
    totalresults = data['total_count']
    return int(totalresults)

def output(results): #Guarda cada resultado de la lista en el dataframe
    gamesdf = pd.concat([pd.DataFrame(g) for g in results])
    gamesdf.to_csv('gamesprices.csv', index=False)
    print('Saved to CSV')
    print(gamesdf.head())
    return

results = []
for x in range(0, totalresults(url), 50):
    data = get_data(f'https://store.steampowered.com/search/results/?query&start={x}&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&tags=19&infinite=1')
    results.append(parse_games(data))
    print('Results Scraped: ', x)
    time.sleep(1.5)

output(results)




