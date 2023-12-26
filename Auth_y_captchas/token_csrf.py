import requests
import json

"""
OBJETIVO: 
-Aprender como usar csrf token para acceder a la data de una pagina
-csrf es un token unico que se genera con cada requerimiento a la pagina
-Buscar tag de tipo input value perteneciente al csrf y luego pasarlo al headers
-
"""

headers = {
    "user-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/119.0.0.0 Safari/537.36'
}

#SI LA PAGINA DETECTA QUE ESE ESTAN HACIENDO MUCHOS REQUERIMIENTOS PONE UN CAPTCHA,
# PONER UN USER AGENT DIFERENTE

#CREAR SESSION

session = requests.Session()

response = session.get("https://www.bolsadesantiago.com", headers=headers)
print(response) #INTENTAR LLENAR COOKIES DE LA PAGINA, NO ES SUFICIENTE

#OBTENER TOKEN CSRF CON API ENCONTRADA

url_token = "https://www.bolsadesantiago.com/api/Securities/csrfToken"
response = session.get(url_token, headers=headers)
token = response.json()['csrf']
print(token)

headers['X-Csrf-Token'] = token


#LLAMAR A LA API

url = "https://www.bolsadesantiago.com/api/Comunes/getHoraMercado" #403, NECESITA TOKEN

response = session.post(url,headers=headers)
print(response) #403
print(response.text)

diccionario = response.json()
print(diccionario)

"""
Para poder extraer la informacion de la hora del mercado de la bolsa de Chile es necesario adquirir el token CSRF generado
ya que la api a la que se pide la informacion esta protegida y no da acceso, es necesario hacer una peticion a la api que genera el token, luego
añadirlo a los headers y hacer el respectivo requerimiento.
"""