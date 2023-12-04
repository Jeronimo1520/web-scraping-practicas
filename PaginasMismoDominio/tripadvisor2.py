from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector


class Opinion(Item):
    titulo = Field()
    calificacion = Field()
    contenido = Field()
    autor = Field()


class TripAdvisor(CrawlSpider):
    name = 'OpinionesUsuarioTripAdvisor'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 100,  # Un poco alto
        'FEED_EXPORT_ENCODING': 'utf-8'  # Para que se muestren bien los caracteres especiales (ej. acentos)
    }
    allowed_domains = ['tripadvisor.com']
    start_urls = ['https://www.tripadvisor.com/Hotels-g303845-Guayaquil_Guayas_Province-Hotels.html']

    download_delay = 1

    rules = (
        # Paginacion de hoteles(h)
        Rule(
            LinkExtractor(
                allow=r'-oa\d+-'  # \d+ patron donde puede ir cualquier numero
            ), follow=True
        ),
        # Detalle hoteles(v)
        Rule(
            LinkExtractor(
                allow=r'/Hotel_Review-',
                restrict_xpaths=['//div[@class="jhsNf N G"]//a[contains(@href,"/Hotel_Review")]']
            ), follow=True
        ),
        # Paginacion de opiniones dentro de un hotel(h)
        Rule(
            LinkExtractor(
                allow=r'-or\d+'
            ), follow=True
        ),
        # detalle perfil de usuario(v)
        Rule(
            LinkExtractor(
                allow=r'/Profile/',
                restrict_xpaths=['//div[@data-test-target="HR_CC_CARD"]//a[contains(@class,"ui_header_link")]']
            ), follow=True, callback='parse_opinion'
        ),
    )
    def obtenerCalificacion(self,texto):
        calificacion = texto.split("_")[-1]
        return calificacion
    def parse_opinion(self, response):
        sel = Selector(response)
        opiniones = sel.xpath('//div[@id="content"]/div/div')
        autor = sel.xpath('//h1/span/text()').get()
        for opinion in opiniones:
            item = ItemLoader(Opinion(), opinion)
            item.add_xpath('titulo', './/div[@class="AzIrY b _a VrCoN"]/text()')
            item.add_xpath('contenido', './/q/text()')
            item.add_xpath('calificacion', './/div[contains(@class, "ui_card section")]//a/div/span[contains(@class, "ui_bubble_rating")]/@class',MapCompose(
                self.obtenerCalificacion
            ))
            item.add_value('autor', autor)

            yield item.load_item()