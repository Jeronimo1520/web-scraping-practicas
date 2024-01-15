from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import io
from PIL import Image
import requests

headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.3"
}
'''
OBJETIVO: 
    - Extraer imagenes de OLX.
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

for i in range(2):
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


#Las imagenes cargan a medida se hace scroll de un anuncio
"""No se puede usar WebDriverWait porque las imagenes no se cargan a menos de que se 
visualice dentro de la pantalla de mi navegador, por lo tanto no funciona"""

driver.execute_script("window.scrollTo({top: 0, behavior: 'smooth'});")
sleep(5)
driver.execute_script("window.scrollTo({top: 20000, behavior: 'smooth'});")
sleep(5)

# Encuentro cual es el XPATH de cada elemento donde esta la informacion que quiero extraer
# Esto es una LISTA. Por eso el metodo esta en plural

anuncios = driver.find_elements('xpath', '//li[@data-aut-id="itemBox"]')

i = 0
for anuncio in anuncios:
    try:
        precio = anuncio.find_element(By.XPATH, './/span[@data-aut-id="itemPrice"]').text
        print(precio)

        titulo = anuncio.find_element(By.XPATH, './/span[@data-aut-id="itemTitle"]').text
        print(titulo)
    except:
        print('Anuncio carece de precio o titulo ')

    try:
        url = anuncio.find_element(By.XPATH, './/img').get_attribute('src')
        print(url)
        # con requests, hago el requerimiento a la URL de la imagen
        image_content = requests.get(url, headers=headers).content
        # PROCESAMIENTO DE LA IMAGEN
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        file_path = './imagenes/' + str(i) + '.jpg'  # nombre a guardar de la imagen
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
    except Exception as e:
        print(e)
        print("Error")
    i += 1
