from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

"""
OBJETIVOS:
Scrapear informacion de los articulos academicos
de Google Scholar
-Es posible el uso de Scrapy, no hay carga dinamica
- Llenar el item con .add_value
    - Aprender el uso de .get() y .getall() para obtener información de la página
"""

class Articulo(Item):
    titulo = Field()
    citaciones = Field()
    autores = Field()
    url = Field()

class GoogleScholar(CrawlSpider):
    name = 'googlescholar'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/119.0.0.0 Safari/537.36',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'DEPTH_LIMIT': 1,
    }

    download_delay = 4

    start_urls = ['https://scholar.google.com/scholar?as_ylo=2023&q=AI&hl=en&as_sdt=0,5']
    allowed_domains = ['scholar.google.com']

    rules = (
        Rule(  # Regla de movimiento VERTICAL hacia las citaciones de dicho articulo
            LinkExtractor(
                restrict_xpaths='.//div[@class="gs_fl gs_flb"]',
                allow=r'\?cites='  # Si la URL contiene este patron, haz un requerimiento a esa URL
            ), follow=True, callback="parse_start_url"),
    # El callback es el nombre de la funcion que se va a llamar con la respuesta al requerimiento hacia estas URLs
    )

    #Para extraer la informacion de la url semillS, tanto como la de los niveles de profundidad
    # se puede llamar parse_start_url a la funcion de extraccion
    def parse_start_url(self, response):
        sel = Selector(response)

        articulos = sel.xpath('.//div[@class="gs_ri"]')

        for articulo in articulos:
            item = ItemLoader(Articulo(), articulo)

            titulo = articulo.xpath('.//h3/a//text()').getall()
            titulo = "".join(titulo)
            item.add_value('titulo', titulo)

            url = articulo.xpath('.//h3/a/@href').get()
            item.add_value('url', url)

            autores = articulo.xpath('.//div[@class="gs_a"]//text()').getall() #Lista de autores
            autores = ''.join(autores)
            autores = autores.split('-')[0].strip()
            item.add_value('autores', autores)

            citaciones = 0
            try:
                citaciones = articulo.xpath('.//a[contains(@href,"cites")]/text()').get()
                citaciones = citaciones.split(' ')[2]
            except:
                pass

            item.add_value('citaciones', citaciones)

            yield item.load_item()
