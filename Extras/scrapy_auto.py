from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.spiders import Spider
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

password = open('password_mongo.txt').readline().strip()
uri = f"mongodb+srv://Jeronimo1520:{password}@cluster0.whzzoqw.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['accuweather']
col = db['clima_scrapy']

class ExtractorClima(Spider):
    name = "CLIMA"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/113.0.0.0 Safari/537.36",
        "LOG_ENABLED": False  # No mostrar todos los logs dentro de la consola
    }

    # Start URLs puede ser un arreglo de muchas URLs. Al no haber reglas, cada una de
    # estas URLs va a ejecutar la funcion parse una vez que se haga el requerimiento y
    # se obtenga una respuesta
    start_urls = [
        "https://www.accuweather.com/es/es/madrid/308526/weather-forecast/308526",
        "https://www.accuweather.com/es/co/medellin/107060/weather-forecast/107060",
        "https://www.accuweather.com/es/ec/quito/129846/weather-forecast/129846?postalcode=undefined"
    ]

    def parse(self, response):
        ciudad = response.xpath('//h1/text()').get()
        current = response.xpath('//div[@class="cur-con-weather-card__panel"]//div[@class="temp"]/text()').get()
        real_feel = response.xpath('//div[@class="cur-con-weather-card__panel"]//div[@class="real-feel"]/text()').get()

        ciudad = ciudad.replace('\n', '').replace('\r', '').strip()
        current = current.replace('°', '').replace('\n', '').replace('\r', '').strip()
        real_feel = real_feel.replace('RealFeel®', ' ').replace('°', ' ').replace('\n', '').replace('\t', '').strip()

        """Actualizacion periodica de datos en MongoDB"""
        col.update_one({
            "ciudad": ciudad  # Mi Identificador
        }, {
            "$set": {
                "current": current,
                "real_feel": real_feel,
                "ciudad": ciudad
            }
        }, upsert=True)

        # No necesito hacer yield. El yield me sirve cuando voy a guardar los datos
        # en un archivo, corriendo Scrapy desde Terminal

        # f = open("./data_clima_scrapy.csv", "a")  # a de agregar
        # f.write(ciudad + "," + current + "," + real_feel + "\n")
        # f.close()


#Automatizacion
runner = CrawlerRunner()
task = LoopingCall(lambda: runner.crawl(ExtractorClima)) #Llamada iterativa, recibe una funcion
task.start(20) #En segundos, cada cuanto se debe ejecutar la tarea
reactor.run()

# Segundos en 1 dia: 86400
# Segundos en 1 hora: 3600
# Segundos en 1 semana: 604800
# Segundos en 1 mes: 2.628e+6
# Segundos en 1 minuto: 60

"""
Lo ideal seria usar un VM en la nube para evitar problemas de red, almacenmaiento, etc
"""