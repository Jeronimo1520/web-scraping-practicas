from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
import scrapeops_scrapy

API_KEY = 'xxxxxxxxxxxxxxx'

"""
OBJETIVO: Extraer nombre y direccion de los apartamentos de Urbania.pe
- Utilizar mas de una url semilla
- Aprender a utilizar Web Scraping en la Nube con CRAWLERA Y ScrapeOps, ya que hay un error 403, acceso no permitido
-ScrapeOps es baneado al tratar de acceder a urbania, error 403
-Intentar Crawlera, pero es de pago
"""


class Apartamento(Item):
    nombre = Field()
    direccion = Field()


class Urbaniape(CrawlSpider):  # Crawlspider porque es scrapy horizontal
    name = "Apartamentos"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/116.0.0.0 Safari/537.36',
        'CLOSESPIDER_ITEMCOUNT': 100,
        'FEED_EXPORT_ENCODING': 'utf-8',
        'SCRAPEOPS_API_KEY': API_KEY,
        'EXTENSIONS': {'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500},
        'DOWNLOADER_MIDDLEWARES': {'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550,
                                   'scrapy.downloadermiddlewares.retry.RetryMiddleware': None}
    }

    # Arreglo armado dinamiacamente
    start_urls = []
    for i in range(1, 6):
        start_urls.append('https://urbania.pe/buscar/proyectos-propiedades?page=' + str(i))
    # Como no se ve una manera de hacer una paginas horizontal clara, se opta por poner todas las url a las que quiero ir

    allowed_domains = ['urbania.pe']

    rules = (
        Rule(
            LinkExtractor(
                allow=r'/proyecto/'
            ), follow=True, callback='parse_apto'
        )
    ),

    def parse_apto(self, response):
        sel = Selector(response)
        item = ItemLoader(Apartamento(), sel)

        item.add_xpath('nombre', '//h1/text()')
        item.add_xpath('direccion', '//p[@class="subtitle"]/text()')

        yield item.load_item()
