from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
import io
from scrapy.crawler import CrawlerRunner, CrawlerProcess
import requests
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

password = open('password_mongo.txt').readline().strip()
uri = f"mongodb+srv://Jeronimo1520:{password}@cluster0.whzzoqw.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['buscalibre']
col = db['libros_envio_express']

"""
OBJETIVO: 
    - Extraer horizontal y verticalmente informacion de los libros de buscalibre.com y guardar data en MongoDB"""


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
        sel = Selector(response)
        nombre = sel.xpath('//p[@class="tituloProducto"]/text()').get()

        autores = sel.xpath('//div[@id="metadata-autor"]/a[@class="color-primary font-weight-medium '
                            'link-underline"]/text()').getall()

        autores = [self.limpiar_texto(autor) for autor in autores]

        editorial = sel.xpath('//div[@id="metadata-editorial"]/a/text()').get()

        precio_actual = sel.xpath('//p[contains(@class,"precioAhora")]/span/text()').get()

        precio_antes = sel.xpath('//p[contains(@class,"precioAntes")]/text()').get()

        if precio_antes:
            precio_antes = self.limpiar_texto(precio_antes)
        else:
            precio_antes = 'N/A'

        descuento = sel.xpath('//div[contains(@class,"box-descuento font")]/strong/text()').get()

        if descuento:
            descuento = self.quitar_porcentaje(descuento)
        else:
            descuento = 'N/A'

        url_imagen = sel.xpath('(//div[@class="imagen"]/img/@src)[1]').get()
        image_content = requests.get(url_imagen).content
        image_file = io.BytesIO(image_content).read()

        col.update_one({
            "nombre": nombre  # Mi Identificador
        }, {
            "$set": {
                "autores": autores,
                "editorial": editorial,
                "precio_actual": precio_actual,
                "precio_antes": precio_antes,
                "descuento": descuento,
                "portada_libro":image_file
            }
        }, upsert=True)
process = CrawlerProcess()
process.crawl(BuscalibreCrawler)
process.start()