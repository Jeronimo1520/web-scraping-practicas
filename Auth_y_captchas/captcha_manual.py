from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep

options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.3")
driver = webdriver.Chrome(options=options)

url = "https://www.google.com/recaptcha/api2/demo"
driver.get(url)

try:
    #El captcha se encuentra dentro de un iframe por lo tanto se cambia el contexto del driver
    driver.switch_to.frame(driver.find_element(By.XPATH,'//iframe'))
    captcha = driver.find_element(By.XPATH, '//div[@class="recaptcha-checkbox-border"]')
    captcha.click()

    input() #El codigo para hasta que se de enter en la terminal

    sleep(3)


    driver.switch_to.default_content()

    submit = driver.find_element(By.XPATH, '//input[@id="recaptcha-demo-submit"]')
    submit.click()

except Exception as e:
    print(e)

contenido = driver.find_element(By.CLASS_NAME,'recaptcha-success')
print(contenido.text)

"""
El captcha manual se debe tener en cuanta en paginas donde el uso de resolver catpchas sea
minimo o sea muy poco, o cuando la informacion sea importante, valiosa o en gran cantidad
donde valga la pena hacer un captcha manual para obtener gran volumen de data.
"""