import random
from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

"""
OBJETIVO: 
    - Selenium en 2023: Objeto service y ChromeDriverManager
    - Selenium en Headless mode (sin navegador)"""

options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.3")
options.add_argument("--headless") # Headless Mode velocidad
driver = webdriver.Chrome(options=options)

driver.get('https://www.airbnb.com.co/')

sleep(3)

listado_anuncion = driver.find_elements(By.XPATH, '//div[@data-testid="listing-card-title"]')

for anuncion in listado_anuncion:
    print(anuncion.text)