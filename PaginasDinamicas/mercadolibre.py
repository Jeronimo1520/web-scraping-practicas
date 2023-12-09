"""
OBJETIVO: 
    - Extraer el precio, titulo y descripcion de productos en Mercado Libre.
    - Aprender a realizar extracciones verticales y horizontales con Selenium.
    - Demostrar que Selenium no es optimo para realizar extracciones que requieren traversar mucho a traves de varias pagina de una web
    - Aprender a manejar el "retroceso" del navegador
    - Aprender a definir user_agents en Selenium"""

"""Ya que selenium no es ideal para realizar extracciones que requieren traversar, se eligira
una url con pocos articulos"""

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Definimos el User Agent en Selenium utilizando la clase Options

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.3")
driver = webdriver.Chrome(options=opts)

#URL
driver.get('https://listado.mercadolibre.com.ec/herramientas-vehiculos/')

# LOGICA DE MAXIMA PAGINACION CON  WHILE
# VECES VOY A PAGINAR HASTA UN MAXIMO DE 10
PAGINACION_MAX = 10
PAGINACION_ACTUAL = 1

sleep(3) #Esperar a que cargue el contenido
while PAGINACION_MAX > PAGINACION_ACTUAL:
    link_productos = driver.find_elements(By.XPATH, "//a[contains(@class,'-link__title-card')]")
    links_pagina = []
    for tag in link_productos:
        links_pagina.append(tag.get_attribute("href"))

    for link in links_pagina:
        try:
            driver.get(link)
            titulo = driver.find_element(By.XPATH, '//h1').text
            precio = driver.find_element(By.XPATH, '//span[@class="andes-money-amount__fraction"]').text
            print(titulo)
            print(precio)
            # driver.back() #Me devuelvo a la pagina anterior
        except Exception as e:
            print(e)
            driver.back()

    try:
        boton_siguiente = driver.find_element(By.XPATH, '//span[text()="Siguiente"]')
        boton_siguiente.click()
    except Exception as e:
        break
    PAGINACION_ACTUAL+=1

"""
CONCLUSIONES:
- La velocidad de la extraccion depende de 3 factores
*La velocidad del internet
*La potencia del computador
*La optimizacion del codigo
-Selenium tarda muchisimo mas en lograr el scraping a mercadolibre que Scrapy
"""