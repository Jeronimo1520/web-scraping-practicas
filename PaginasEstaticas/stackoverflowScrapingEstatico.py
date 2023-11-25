import requests
from bs4 import BeautifulSoup

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu "
                  "Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
}

url = "https://stackoverflow.com/questions"

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")

"""Objetivo: Extrer el titulo y la descripcion de cada una de las preguntas de la pagina
principal de StackOverflow/questions"""

questions_container = soup.find("div", id="questions")

questions_list = questions_container.find_all("div", class_="s-post-summary")

for question in questions_list:
    # question_title = question.find("h3").text
    element_question_title = question.find("h3")
    question_title = element_question_title.text
    question_description= element_question_title.find_next_sibling("div").text
    # question_description = question.find(class_='s-post-summary--content-excerpt').text
    question_description = question_description.replace('\n', '').replace('\r', '')
    print(question_title)
    print(question_description)
