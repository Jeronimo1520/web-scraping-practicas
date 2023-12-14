from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy import Request

"""
OBJETIVO: Aprender a extraer informacion dentro de un iframe en una pagina web
"""

class Dummy(Item):
    titulo = Field()
    titulo_iframe = Field()


class W3SCrawler(Spider):
    name = 'w3s'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/119.0.0.0 Safari/537.36',
        'REDIRECT_ENABLED': True  # Parametro para activar los redirects (codigo 302)
    }

    allowed_domains = ['w3schools.com']

    start_urls = ['https://www.w3schools.com/html/html_iframe.asp']

    download_delay = 2

    def parse(self, response):
        sel = Selector(response)
        titulo = sel.xpath('//div[@id="main"]//h1/span/text()').get()

        meta_data={
            'titulo': titulo
        }

        iframe_url = sel.xpath('//div[@id="main"]//iframe[@width="99%"]/@src').get()

        iframe_url = 'https://www.w3schools.com/html/'+ iframe_url

        yield Request(iframe_url,
                      callback= self.parse_iframe,
                      meta=meta_data# Debido a que el item no se puede cargar hasta que yo no tenga los datos que obtendre en el request al iframe, tengo que pasar los datos obtenidos en esta pagina, al siguiente request
                      )

    def parse_iframe(self,response):
        item = ItemLoader(Dummy(), response)
        item.add_xpath('titulo_iframe', '//div[@id="main"]//h1/span/text()')
        item.add_value('titulo', response.meta.get('titulo'))
        yield item.load_item()