import scrapy
from scrapy.crawler import CrawlerProcess

class EventSpider(scrapy.Spider):
    name = "event"

    def start_requests(self):
        urls = {
            self.abakus_parse : "https://Abakus.no/events"
        }

        for yield_func in urls.keys():
            url = urls.get(yield_func)
            yield scrapy.Request(url=url, callback=yield_func)

    
    def abakus_parse(self, response):
        print(response.body) 

if __name__ == '__main__':
    spider = EventSpider()
    process = CrawlerProcess()
    process.crawl(EventSpider)
    process.start()