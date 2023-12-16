import requests
from lxml import html

headers = {
    "user-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/119.0.0.0 Safari/537.36'
}

login_form_url = "https://github.com/login"

session = requests.Session()

login_form_res = session.get(login_form_url, headers=headers)

parser = html.fromstring(login_form_res.text)

token = parser.xpath("//input[@name='authenticity_token']/@value")
login_url = "https://github.com/session"

login_data = {
    "login": "jeronimo1520",
    "password": open('./password.txt').readline().strip(),
    "commit": "Sign in",
    "authenticity_token": token
}

session.post(
    login_url,
    data=login_data,
    headers=headers
)

data_url = "https://github.com/Jeronimo1520?tab=repositories"

respuesta = session.get(
    data_url,
    headers=headers
)

parser = html.fromstring(respuesta.content)

repositorios = parser.xpath('//h3[@class="wb-break-all"]/a/text()')

for repositorio in repositorios:
    print(repositorio)
