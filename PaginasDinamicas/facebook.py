from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from time import sleep
import pandas as pd

"""
OBJETIVO: Extraer informacion de post de Facebook de la pagina de Koaj
- Post cargan dinamicamente
- Scroll debe ser suavizado
- Árbol HTML caótico
- Modal de aceptar Cookies e iniciar sesion
-Arbol HTML cambiante, actualizar xpaths si es necesario
"""


def scrolling_suavizado(driver, iteracion):
    bajar_hasta = 2000 * (iteracion + 1)
    inicio = (2000 * iteracion)
    for i in range(inicio, bajar_hasta, 5):
        scrolling_script = f"""window.scrollTo(0,{i})"""
        driver.execute_script(scrolling_script)


opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/119.0.0.0 Safari/537.3")
driver = webdriver.Chrome(options=opts)

driver.get("https://www.facebook.com/modakoaj")

sleep(2)

try:
    boton_cookies = driver.find_element(By.XPATH, '//div[not(@aria-disabled) and @aria-label="Allow all cookies"]')
    boton_cookies.click()
except:
    print("Modal de permitir cookies no encontrado")

cerrar_dialogo = driver.find_element(By.XPATH, '//div[@aria-label="Close"]')
cerrar_dialogo.click()
sleep(0.5)

n_scrolls = 0
max_scrolls = 10
max_post = 5

posts = driver.find_elements(By.XPATH, '//div[@role="article" and @aria-describedby]')

while len(posts) < max_post and n_scrolls < max_scrolls:
    scrolling_suavizado(driver, n_scrolls)
    n_scrolls += 1
    posts = driver.find_elements(By.XPATH, '//div[@role="article" and @aria-describedby]')
    sleep(2)

posts = driver.find_elements(By.XPATH, '//div[@role="article" and @aria-describedby]')
for post in posts:
    texto_post = post.find_element(By.XPATH, '(.//div[@data-ad-comet-preview="message"])[1]').text

    url_post = post.find_element(By.XPATH, './/span[@id]//a[@aria-label]').get_attribute('href')

    reacciones = post.find_element(By.XPATH, './/span[@class="x1e558r4"]').text

    comentarios_compartidos = post.find_elements(By.XPATH, './/div[@class="x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf '
                                                           'x2lah0s x193iq5w xeuugli xg83lxy x1h0ha7o x10b6aqq '
                                                           'x1yrsyyn"]')

    n_comentarios = 0
    n_compartidos = 0
    if len(comentarios_compartidos) == 2:
        n_comentarios = comentarios_compartidos[0].text
        n_compartidos = comentarios_compartidos[1].text
    elif len(comentarios_compartidos) == 0:
        n_comentarios = 0
        n_compartidos = 0
    else:
        text_comentarios = post.find_elements(By.XPATH, '//span[text()="Ver más comentarios"]')
        existen_comentarios = len(text_comentarios) > 0
        if existen_comentarios:
            n_comentarios = comentarios_compartidos[0].text
        else:
            n_compartidos = comentarios_compartidos[0].text
    print(texto_post)
    print('Reacciones: ', reacciones)
    print('N comentarios: ', n_comentarios)
    print('N compartidas: ', n_compartidos)
    print('URL post: ', url_post)
