from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor

"""
OBJETIVO: 
    - Extraer horizontal y verticalmente información de artículos de marcadolibre"""


class Article(Item):
    title = Field()
    price = Field()
    description = Field()


class MercadoLibreCrawler(CrawlSpider):
    name = 'mercadoLibre'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/108.0.0.0 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 20
    }

    download_delay = 2

    allowed_domains = ['listado.mercadolibre.com.co', 'mercadolibre.com.co', 'articulo.mercadolibre.com.co']

    start_urls = ['https://listado.mercadolibre.com.co/guitarra-acustica']

    rules = (
        # Paginacion
        Rule(LinkExtractor(allow=(), restrict_xpaths='//li[contains(@class,"andes-pagination__button--next")]/a')),
        # Detalle de productos
        Rule(
            LinkExtractor(allow=(), restrict_xpaths=(
                '//a[@class="ui-search-item__group__element ui-search-link"]')),
            follow=True,
            callback="parse_items"
        ),
    )

    def limpiar_texto(self, texto):
        nuevo_texto = texto.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
        return nuevo_texto

    def parse_items(self, response):
        # if 'https://www.mercadolibre.com.co/navigation/addresses' not in response.url:
        item = ItemLoader(Article(), response)
        item.add_xpath('title', '//h1[@class="ui-pdp-title"]/text()', MapCompose(self.limpiar_texto))
        item.add_xpath('description',
                       '//p[@class="ui-pdp-description__content"]/text()', MapCompose(self.limpiar_texto))
        item.add_xpath('price', '(//span[@class="andes-money-amount__fraction"])[1]/text()')

        yield item.load_item()
