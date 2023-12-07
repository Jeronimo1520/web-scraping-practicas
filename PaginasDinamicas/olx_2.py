from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

'''
OBJETIVO: 
    - Extraer el precio y el titulo de los anuncios en la pagina de OLX.
    - Aprender a realizar extracciones que requieran una accion de click para cargar datos.
    - Aprender a utilizar la espera por eventos de Selenium.
    - Aprender a optimizar el tiempo de ejecucion de nuestras extracciones por Selenium de manera inteligente
    '''

options = Options()
options.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.3")
options.page_load_strategy = 'normal'

# Instancio el driver de selenium que va a controlar el navegador
# A partir de este objeto voy a realizar el web scraping e interacciones
driver = webdriver.Chrome(options=options)

driver.get('https://www.olx.in')
sleep(2)
driver.refresh()  # Solucion de un bug extraño en Windows en donde los anuncios solo cargan al hacerle refresh a la página
sleep(2)

# Busco el boton para cargar mas informacion

for i in range(3):
    try:
        # Esperamos a que el boton se encuentre disponible a traves de una espera por eventos
        # Espero un maximo de 10 segundos, hasta que se encuentre el boton dentro del DOM
        boton = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[@data-aut-id="btnLoadMore"]')
                                           ))
        boton.click()
        nAnuncios = 20 + ((i + 1) * 20)  # 20 anuncios de carga inicial, y luego 20 anuncios por cada click que he dado
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//li[@data-aut-id="itemBox"]//span[@data-aut-id="itemPrice"]'))
        )
    except:
        break

# Encuentro cual es el XPATH de cada elemento donde esta la informacion que quiero extraer
# Esto es una LISTA. Por eso el metodo esta en plural

anuncios = driver.find_elements(By.XPATH, '//li[@data-aut-id="itemBox"]')

for anuncio in anuncios:
    try:
        precio = anuncio.find_element(By.XPATH, './/span[@data-aut-id="itemPrice"]').text
        print(precio)

        titulo = anuncio.find_element(By.XPATH, './/span[@data-aut-id="itemTitle"]').text
        print(titulo)
    except:
        print('Anuncio carece de precio o titulo ')
