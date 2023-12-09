from time import sleep
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

"""
OBJETIVO: 
    - Extraer resenas escritas por usuarios en Google Places.
    - Aprender a cargar informacion haciendo scrolling.
    - Aprender a manejar varios tabs abiertos al mismo tiempo en Selenium."""



opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.3")
driver = webdriver.Chrome(options=opts)

driver.get('https://www.google.com/maps/place/Restaurante+Amazonico/@40.423706,-3.6872655,17z/data=!4m7!3m6!1s0xd422899dc90366b:0xce28a1dc0f39911d!8m2!3d40.423706!4d-3.6850768!9m1!1b1')

sleep(random.uniform(4.0, 5.0))

def getScrollingScript(iteration):
    scrollingScript = """ 
      document.getElementsByClassName('m6QErb DxyBCb kA9KIf dS8AEf')[0].scroll(0, 20000)
    """
    return scrollingScript.replace('20000', str(20000 * (iteration + 1)))

SCROLLS = 0
while SCROLLS != 3:
    driver.execute_script(getScrollingScript(SCROLLS))
    sleep(random.uniform(5.0,6.0))
    SCROLLS += 1

restaurantReviews = driver.find_elements(By.XPATH,'//div[@data-review-id and not(@aria-label)]')

for review in restaurantReviews:
    sleep(1)
    userLink = review.find_element(By.XPATH,".//div[contains(@class, 'WNx')]//button")

    try:
        userLink.click()
        # Window handles contiene una lista con todas las pestanas y ventanas que se encuentran abiertas
        driver.switch_to.window(driver.window_handles[1])

        userReviews = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-review-id and not(@aria-label)]'))
            # Existe el atributo data-review-id Y no existe el atributo aria-label
        )

        USER_SCROLLS = 0
        while USER_SCROLLS != 2:
            driver.execute_script(getScrollingScript(USER_SCROLLS))
            sleep(random.uniform(4.0, 5.0))
            USER_SCROLLS += 1

        userReviews = driver.find_elements(By.XPATH, '//div[@data-review-id and not(@aria-label)]')

        for userReview in userReviews:
            reviewRating = userReview.find_element(By.XPATH, './/span[@class="kvMYJc"]').get_attribute('aria-label')
            userParsedRating = float(''.join(filter(str.isdigit or str.isspace, reviewRating)))  # Solo digitos
            reviewText = ""
            try:
                reviewText = userReview.find_element(By.XPATH, './/span[@class="wiI7pd"]').text
            except:
                print("Review sin texto")
            print(userParsedRating)
            print(reviewText)

            # Cerrar el tab abierto de las review de un usuario
        driver.close()
            # Movemos el contexto del driver al unico tab abierto, es decir el primero
        driver.switch_to.window(driver.window_handles[0])

    except Exception as e:
        print(e)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
