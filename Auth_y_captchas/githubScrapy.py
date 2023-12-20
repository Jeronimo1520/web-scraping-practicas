from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess
import scrapy

class LoginSpider(Spider):
    name = "GithubLogin"

    start_urls = ["https://github.com/login"]

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                "login": "jeronimo1520",
                "password": open('./password.txt').readline().strip(),
            },
            callback = self.after_login
        )

    def after_login(self, response):
        request = scrapy.Request(
            "https://github.com/Jeronimo1520?tab=repositories", #Requerimiento forzozo
            callback=self.parse_repos
        )
        yield request

    def parse_repos(self, response):
        sel = Selector(response)
        repos = sel.xpath('//h3[@class="wb-break-all"]/a/text()')
        for repo in repos:
            print(repo.get()) #GET ME OBTIENE EL TEXTO

process = CrawlerProcess()
process.crawl(LoginSpider)
process.start()