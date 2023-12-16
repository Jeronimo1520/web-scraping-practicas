from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector


"""
OBJETIVO: 
    - Extraer horizontal y verticalmente informacion de los libros de buscalibre.com"""

class Libro(Item):
    nombre = Field()
    autor = Field()
    precioActual = Field()
    precioAntes = Field()
    editorial = Field()
    descuento = Field()

class BuscalibreCrawler(CrawlSpider):
    name = 'buscalibre'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/119.0.0.0 Safari/537.36',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'CLOSESPIDER_PAGECOUNT': 50
    }

    download_delay = 2

    allowed_domains = ['buscalibre.com.co']

    start_urls = ['https://www.buscalibre.com.co/libros-envio-express-colombia_t.html']

    rules = (
        # Paginacion
        Rule(LinkExtractor(allow=(), restrict_xpaths='//a[@id="pagnNextLink"]')),
        # Detalle de productos
        Rule(
            LinkExtractor(allow=(), restrict_xpaths=(
                '//div[contains(@class,"box-producto")]/a')),
            follow=True,
            callback="parse_libros"
        ),
    )
    def limpiar_texto(self, texto):
        nuevo_texto = texto.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
        return nuevo_texto

    def quitar_porcentaje(self, texto):
        return texto.replace("%", "")

    def parse_libros(self, response):
        item = ItemLoader(Libro(), response)
        item.add_xpath('nombre', '//p[@class="tituloProducto"]/text()')

        sel = Selector(response)
        autores = sel.xpath('//div[@id="metadata-autor"]/a[@class="color-primary font-weight-medium '
                            'link-underline"]/text()').getall()

        item.add_value('autor', [self.limpiar_texto(autor) for autor in autores])
        item.add_xpath('precioActual','//p[contains(@class,"precioAhora")]/span/text()')

        precio_antes = sel.xpath('//p[contains(@class,"precioAntes")]/text()').get()
        if precio_antes:
            item.add_value('precioAntes', precio_antes, MapCompose(self.limpiar_texto))
        else:
            item.add_value('precioAntes', 'N/A')

        item.add_xpath('editorial', '//div[@id="metadata-editorial"]/a/text()')
        descuento = sel.xpath('//div[contains(@class,"box-descuento font")]/strong/text()').get()
        if descuento:
            item.add_value('descuento', descuento, MapCompose(self.quitar_porcentaje))
        else:
            item.add_value('descuento','N/A')
        yield item.load_item()


