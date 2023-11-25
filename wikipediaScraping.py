import requests
from lxml import html

# Redefinir el user agent, para evitar que la identifiquen como roboto

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}
url = "https://www.wikipedia.org/"

response = requests.get(url, headers=headers)

parser = html.fromstring(response.text)

english = parser.get_element_by_id("js-link-box-en")
print(english.text_content())

english = parser.xpath("//a[@id='js-link-box-en']/strong/text()")
print(english)

languages = parser.xpath("//div[contains(@class,'central-featured-lang')]//strong/text()")
for lan in languages:
    print(lan)

languages = parser.find_class("central-featured-lang")
for lan in languages:
    print(lan.text_content())  # Obtener el texto
