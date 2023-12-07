import random
from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

'''
OBJETIVO: 
    - Extraer el precio y el titulo de los anuncios en la pagina de OLX autos.
    - Aprender a realizar extracciones que requieran una accion de click para cargar datos.
    - Introducirnos a la logica de Selenium'''

options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.3")
options.page_load_strategy = 'normal'

# Instancio el driver de selenium que va a controlar el navegador
# A partir de este objeto voy a realizar el web scraping e interacciones
driver = webdriver.Chrome(options=options)

driver.get('https://www.olx.in/cars_c84')
sleep(2)
driver.refresh() # Solucion de un bug extraño en Windows en donde los anuncios solo cargan al hacerle refresh a la página
sleep(2)

# Busco el boton para cargar mas informacion

boton = driver.find_element(By.XPATH, '//button[@data-aut-id="btnLoadMore"]')
for i in range(3):
    try:
        boton.click()
        sleep(random.uniform(8.0,10.0))
        # busco el boton nuevamente para darle click en la siguiente iteracion
        boton = driver.find_element(By.XPATH, '//button[@data-aut-id="btnLoadMore"]')
    except:
        break

# Encuentro cual es el XPATH de cada elemento donde esta la informacion que quiero extraer
# Esto es una LISTA. Por eso el metodo esta en plural

autos = driver.find_elements(By.XPATH, '//li[@data-aut-id="itemBox"]')

for auto in autos:
    try:
        precio = auto.find_element(By.XPATH,'.//span[@data-aut-id="itemPrice"]').text
        print(precio)

        titulo = auto.find_element(By.XPATH, './/div[@data-aut-id="itemTitle"]').text
        print(titulo)
    except:
        print('Anuncio carece de precio o titulo ')

