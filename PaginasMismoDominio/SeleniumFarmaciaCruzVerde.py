from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

password = open('password_mongo.txt').readline().strip()
uri = f"mongodb+srv://Jeronimo1520:{password}@cluster0.whzzoqw.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['cruz_verde']
col = db['medicamentos']

"""
OBJETIVO: 
    - Extrer informacion de los medicamentos de farmacia Cruz Verde"""

options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.3")
driver = webdriver.Chrome(options=options)


driver.get('https://www.cruzverde.com.co/medicamentos/')

PAGINACION_MAX = 4
PAGINACION_ACTUAL = 1

driver.refresh()

sleep(10) #Esperar a que cargue el contenido


def quitar_porcentaje(texto):
    return texto.replace("%", "")

while PAGINACION_MAX > PAGINACION_ACTUAL:
    sleep(10)
    listado_medicamentos = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, '//div[@class="flex flex-col h-full p-10 bg-white rounded-sm font-open sm:p-10"]'))
    )
    for medicamento in listado_medicamentos:
        try:
            nombre_medicamento = medicamento.find_element(By.XPATH, './/span[@class="ng-star-inserted"]').text
            precio = medicamento.find_element(By.XPATH, './/span[@class="font-bold text-prices"]').text
            col.insert_one({
                'nombre_medicamento': nombre_medicamento,
                'precio': quitar_porcentaje(precio)
            })
        except Exception as e:
            print(e)
    try:
        paginas = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class,'rounded-full flex items-center ')]"))
        )
        for pagina in paginas:
            if pagina.text == str(PAGINACION_ACTUAL + 1):
                pagina.click()
    except Exception as e:
        break
    PAGINACION_ACTUAL += 1
