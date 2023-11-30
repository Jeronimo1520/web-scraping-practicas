from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.loader import ItemLoader

"""
OBJETIVO: 
    - Extraer las noticias de la seccion de deportes de Diario El Universo"""


class Article(Item):
    id = Field()
    title = Field()
    description = Field()
    category = Field()


class ElUniversoSpider(Spider):
    name = "ElUniversoSpider"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu '
                      'Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
    }

    start_urls = ['https://www.eluniverso.com/deportes/']

    def parse(self, response):
        sel = Selector(response)
        articles = sel.xpath('(//ul[@class="feed | divide-y relative  "])[2]/li')  # Mi iterable
        for i, article in enumerate(articles):
            item = ItemLoader(Article(), article)
            item.add_xpath('title', './/h2/a/text()')
            item.add_xpath('description', './/p/text()')
            item.add_xpath('category',
                           './/a[@class="primary_section | font-secondary text-silver-500 dark:text-silver-200 '
                           'uppercase"]/text()')
            item.add_value('id', i)

            yield item.load_item()
        # IMPLEMENTACION CON BS4 JUNTO A SCRAPY, AUMENTA LA COMPLEJIDAD:
        # ME TRAE SECCION DE COLUMNISTAS Y ALGUNAS REPETIDAS, datos en dataElUniverso2.json
        #
        # soup = BeautifulSoup(response.body, 'html.parser')
        # articles_container = soup.find_all(class_='feed | divide-y relative')
        # id = 0
        # for container in articles_container:
        #     articles = container.find_all(class_='relative', recursive = False)
        #     for article in articles:
        #         item = ItemLoader(Article(), response.body)
        #         title = article.find('h2').text.replace('\n', '').replace('\r', '')
        #         description = article.find('p')
        #         if description:
        #             item.add_value('description', description.text.replace('\n', '').replace('\r', ''))
        #         else:
        #             item.add_value('description', 'N/A')
        #         category = article.find('a', class_='primary_section | font-secondary text-silver-500 dark:text-silver-200 uppercase').text
        #         item.add_value('title', title)
        #
        #         item.add_value('category', category)
        #         id +=1
        #         item.add_value('id', id)
        #         yield item.load_item()

        # CORRIENDO SCRAPY SIN LA TERMINAL
        # process = CrawlerProcess({
        #     'FEED_FORMAT': 'json',
        #     'FEED_URI': 'datos_de_salida.json'
        # })
        # process.crawl(ElUniversoSpider)
        # process.start()
