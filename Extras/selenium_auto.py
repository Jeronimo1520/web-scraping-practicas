import schedule
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

password = open('password_mongo.txt').readline().strip()
uri = f"mongodb+srv://Jeronimo1520:{password}@cluster0.whzzoqw.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['accuweather']
col = db['clima']

start_urls = [
    "https://www.accuweather.com/es/es/madrid/308526/weather-forecast/308526",
    "https://www.accuweather.com/es/co/medellin/107060/weather-forecast/107060",
    "https://www.accuweather.com/es/ec/quito/129846/weather-forecast/129846?postalcode=undefined"
]


def extraer_datos():
    options = Options()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/119.0.0.0 Safari/537.3")
    driver = webdriver.Chrome(options=options)

    for url in start_urls:
        driver.get(url)

        ciudad = driver.find_element(By.XPATH, '//h1').text
        current = driver.find_element(By.XPATH, '//div[@class="cur-con-weather-card__panel"]//div[@class="temp"]').text
        real_feel = driver.find_element(By.XPATH,
                                        '//div[@class="cur-con-weather-card__panel"]//div[@class="real-feel"]').text

        ciudad = ciudad.replace('\n', '').replace('\r', '').strip()
        current = current.replace('°C', '').replace('\n', '').replace('\r', '').strip()
        real_feel = real_feel.replace('RealFeel®', ' ').replace('°', ' ').replace('\n', '').replace('\t', '').strip()

        """Actualizacion periodica de datos en MongoDB"""
        col.update_one({
            "ciudad": ciudad #Mi Identificador
        }, {
            "$set": {
                "current": current,
                "real_feel": real_feel,
                "ciudad":  ciudad
            }
        }, upsert=True)
        # Upsert: En caso de que la condicion no cumpla con ningun documento en la coleccion, inserta un nuevo documento

    driver.close()


extraer_datos()
schedule.every(1).minutes.do(extraer_datos)

while True:
    schedule.run_pending()
    time.sleep(1)

'''
Extraccion incremental: Extraccion que ocurre en diferentes momentos de tiempo. De tal manera de que no extraiga
informacion repetida, si no solamente informacion nueva, pudiendo al mismo tiempo actualizar informacion ya extraida
'''
