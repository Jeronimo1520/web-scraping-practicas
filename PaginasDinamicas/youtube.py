from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from time import sleep
import pandas as pd
"""
OBJETIVO: Extraer comentarios de videos de una playlist de Youtube con la ayuda de Selenium
-Tener en cuenta que paginas como Youtube cambian constantemente
PASOS:
-Cerrar disclaimer
-Obtener URL de videos
-Carga de comentarios con Scrolling
-Extraccion de comentarios
"""

def getScrollingScript(iteration):
    scrollingScript = """ 
        window.scrollTo(0,20000)
    """
    return scrollingScript.replace('20000', str(20000 * (iteration + 1)))

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/119.0.0.0 Safari/537.3")
driver = webdriver.Chrome(options=opts)

driver.get("https://www.youtube.com/playlist?list=PLuaGRMrO-j-8NndtkHMA7Y_7798tdJWKH")

sleep(2)

try:
    botton_disclaimer = driver.find_element(By.XPATH, '//button[@aria-label="Accept all"]')
except:
    print("Disclaimer no presente en la página")

videos = driver.find_elements(By.XPATH,'//div[@id="contents"]/ytd-playlist-video-renderer')
urls_videos = []
for video in videos:
    url = video.find_element(By.XPATH,'.//h3/a[@id="video-title"]').get_attribute('href')
    urls_videos.append(url)
print(urls_videos)

# Crear un DataFrame vacío
df = pd.DataFrame(columns=['Comentarios'])

for url in urls_videos:
    driver.get(url)
    sleep(3)
    #El texto de la cantidad de comentario solo se carga cuando el usuario lo ve
    #Hay que hacer scroll hasta que sea visible y luego seguir scrolleando
    driver.execute_script("window.scrollTo(0,400)")

    num_comentarios = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//h2[@id="count"]//span[1]')))
    sleep(3)
    num_comentarios = num_comentarios.text
    num_comentarios = int(num_comentarios) * 0.90 #90% del total de comentarios
    print('Comentarios totales: ', num_comentarios)

    comentarios_cargados = driver.find_elements(By.XPATH, '//yt-formatted-string[@id="content-text"]')

    n_scrolls = 0
    n_scrolls_maximo = 10
    while (len(comentarios_cargados) < num_comentarios) and (n_scrolls < n_scrolls_maximo):
        driver.execute_script(getScrollingScript(n_scrolls))
        n_scrolls += 1
        sleep(2)
        comentarios_cargados = driver.find_elements(By.XPATH, '//yt-formatted-string[@id="content-text"]')

    comentarios_cargados = driver.find_elements(By.XPATH, '//yt-formatted-string[@id="content-text"]')
    for comentario in comentarios_cargados:
        texto_comentario = comentario.text
        print(texto_comentario)

        # Crear un nuevo DataFrame con la fila a agregar
        nueva_fila = pd.DataFrame({'Comentarios': [texto_comentario]})

        # Agregar la nueva fila al DataFrame existente usando concat()
        df = pd.concat([df, nueva_fila], ignore_index=True)

# Eliminar comentarios duplicados en el DataFrame final si los hay
df = df.drop_duplicates()

# Guardar el DataFrame en un archivo CSV
df.to_csv('comentarios_totales.csv', index=False)