from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor

"""
OBJETIVO: 
    - Extraer informacion de hoteles de la ciudad de Medellin de TripAdvisor"""


class Hotel(Item):
    name = Field()
    score = Field()  # El precio ahora carga dinamicamente. Por eso ahora obtenemos el score del hotel
    description = Field()
    amenities = Field()


class TripAdvisor(CrawlSpider):  # Para web scraping vertical y horizontal usamos crawlspider
    name = 'Hotels_Medellin'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/108.0.0.0 Safari/537.36',
        'CLOSESPIDER_ITEMCOUNT': 15
    }

    start_urls = ['https://www.tripadvisor.co/Hotels-g297478-Medellin_Antioquia_Department-Hotels.html']

    download_delay = 2
    # Tupla de reglas para direccionar el movimiento de nuestro Crawler a traves de las paginas
    rules = (
        # Definicion de a que links dentro de la URL semilla mi spider tiene o no que ir por informacion, las reglas son
        # basadas en patrones.
        Rule(
            LinkExtractor(
                allow=r'/Hotel_Review'
            ), follow=True, callback="parse_hotel"  # Funcion a ejecutar cuando se hace un request con el patron
        ),
    )

    # Funcion a utilizar con MapCompose para realizar limpieza de datos
    def quitar_coma(self, texto):
        return texto.replace(",", "")

    def parse_hotel(self, response):
        sel = Selector(response)
        item = ItemLoader(Hotel(), sel)

        item.add_xpath('name', '//h1[@id="HEADING"]/text()')
        item.add_xpath('score', './/div[@class="grdwI P"]/span/text()',
                       MapCompose(self.quitar_coma))
        item.add_xpath('description', '//div[@class="ui_column  "]//div[contains(@data-ssrev-handlers, '
                                      '"Description")]//text()',
                       MapCompose(lambda i: i.replace('\n', '').replace('\r', '')))
        item.add_xpath('amenities', '//div[contains(@data-test-target,"amenity_text")]/text()')

        yield item.load_item()
