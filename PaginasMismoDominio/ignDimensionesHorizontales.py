from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

"""
OBJETIVO: 
    - Extraer informacion sobre Articulos, Reviews y Videos en IGN
    - Aprender a realizar extracciones de informacion de diferente tipo al mismo tiempo
    - Aprender a realizar extracciones verticales y horizontales utilizando reglas
    - Aprender a realizar extracciones con dos dimensiones de horizontalidad
"""
class Article(Item):
    title = Field()
    content = Field()


class Review(Item):
    title = Field()
    score = Field()


class Video(Item):
    title = Field()
    publication_date = Field()


class IGNCrawler(CrawlSpider):
    name = 'ign'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 100,  # Un poco alto
        'FEED_EXPORT_FIELDS': ['title', 'score', 'publication_date', 'content'],
        'FEED_EXPORT_ENCODING': 'utf-8'  # Para que se muestren bien los caracteres especiales (ej. acentos)
    }
    allowed_domains = ['latam.ign.com']
    start_urls = ['https://latam.ign.com/se/?model=article&q=ps5']
    download_delay = 1

    rules = (
        # Horizontaldad por tipo de informacion  # HORIZONTALIDAD POR TIPO => No tiene callback ya que aqui no voy a extraer datos
        Rule(
            LinkExtractor(
                allow=r'type='
            ), follow=True
        ),
        # Horizontalidad por paginacion # HORIZONTALIDAD DE PAGINACION EN CADA TIPO => No tiene callback ya que aqui no voy a extraer datos
        Rule(
            LinkExtractor(
                allow=r'&page=\d+',
            ), follow=True
        ),
        # Una regla por cada tipo de contenido donde ire verticalmente
        # Reviews
        Rule(
            LinkExtractor(
                allow=r'/review/'
            ), follow=True, callback='parse_review'
        ),
        # videos
        Rule(
            LinkExtractor(
                allow=r'/video/'
            ), follow=True, callback='parse_video'
        ),
        # articulos
        Rule(
            LinkExtractor(
                allow=r'/news/'
            ), follow=True, callback='parse_news'
        )

    )

    def limpiar_texto(self, texto):
        nuevo_texto = texto.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
        return nuevo_texto

    def parse_news(self, response):
        item = ItemLoader(Article(), response)
        item.add_xpath('title', '//h1/text()')
        item.add_xpath('content', '//div[@id="id_text"]//*/text()',MapCompose(self.limpiar_texto)) #Buscar en todos los hijos, cualquier tag y sacarle el texto

        yield item.load_item()

    def parse_review(self, response):
        item = ItemLoader(Review(), response)
        item.add_xpath('title', '//h1/text()')
        item.add_xpath('score', '//div[@class="review"]//span[@class="side-wrapper side-wrapper '
                                'hexagon-content"]/div/text()')

        yield item.load_item()

    def parse_video(self, response):
        item = ItemLoader(Video(), response)
        item.add_xpath('title', '//h1/text()')
        item.add_xpath('publication_date', '//span[@class="publish-date"]/text()')

        yield item.load_item()