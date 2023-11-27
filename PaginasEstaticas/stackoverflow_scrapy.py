"""
OBJETIVO: 
    - Extraer las preguntas de la pagina principal de Stackoverflow con Scrapy"""

#Scrapy pagina estatica con scrapy

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader

# ABSTRACCION DE DATOS A EXTRAER - DETERMINA LOS DATOS QUE TENGO QUE LLENAR Y QUE ESTARAN EN EL ARCHIVO GENERADO
class Question(Item):
    id = Field()
    title = Field()
    # description = Field()


# CLASE CORE - SPIDER
class StackOverflowSpider(Spider):
    name = "MiPrimerSpider"  # nombre, puede ser cualquiera

    # Forma de configurar el USER AGENT en scrapy
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
    }

    # URL SEMILLA
    start_urls = ['https://stackoverflow.com/questions']

    # Funcion que se va a llamar cuando se haga el requerimiento a la URL semilla
    def parse(self, response):
        # Selectores: Clase de scrapy para extraer datos
        sel = Selector(response)
        titulo_de_pagina = sel.xpath('//h1/text()').get()
        print(titulo_de_pagina)
        # Selector de varias preguntas
        questions = sel.xpath('//div[@id="questions"]//div[contains(@class,"s-post-summary ")]')
        i = 0
        for question in questions:
            item = ItemLoader(Question(),
                              question)  # Instancio mi ITEM con el selector en donde estan los datos para llenarlo

            # Lleno las propiedades de mi ITEM a traves de expresiones XPATH a buscar dentro del selector "pregunta"
            item.add_xpath('title', './/h3/a/text()')
            # item.add_xpath('description', './/div[@class="s-post-summary--content-excerpt"]/text()')
            item.add_value('id', i)
            i += 1
            yield item.load_item()  # Hago Yield de la informacion para que se escriban los datos en el archivo

# EJECUCION EN TERMINAL:
# scrapy runspider 3_stackoverflow.py -o resultados.csv -t csv