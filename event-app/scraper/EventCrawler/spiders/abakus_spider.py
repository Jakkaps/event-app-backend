import scrapy
import datetime
import pytz
from scraper.EventCrawler.items import EventItem
from scrapy.crawler import CrawlerProcess

class AbakusSpider(scrapy.Spider):
    name = "abakus"
    use_selenium = True
    start_urls = [
        "https://abakus.no/events",
    ]

    def parse(self, response):
        """
        Goes to 'abakus.no/events/' and starts another process on each individual events it finds
        """
 
        for event in response.xpath("//descendant::div[@class='styles__eventItem--2c-Z_4PWb2']"):
            url = "https://abakus.no" + event.xpath("./div[1]/a/@href").get()
            yield scrapy.Request(url=url, callback=self.parse_event)

    def parse_event(self, response):
        """
        Gets information from and individual abakus event-page
        """
        
        event_item = EventItem()
                
        event_item['url'] = response.request.url
        event_item['name'] = response.xpath(".//h2[@class='ContentHeader__header--2o7lNZxfWI EventDetail__title--13hgFeanVH']/text()").get()
        event_item['location'] = response.xpath(".//span[contains(text(), 'Finner sted i')]/following-sibling::strong/text()").get()
        event_item['image_source'] = response.xpath(".//div[@class='Content__cover--26DXPSf5Zo utilities__contentContainer--3A4ds4UtSA utilities__container--2q0U2oWNNe']/img/@src").get()

        description = ""
        for paragraph in response.xpath("//span[@data-text='true']/text()"):
             description += paragraph.get().replace("\n", "").replace("'", "")
        event_item['description'] = "".join(description)

        type = response.xpath(".//span[contains(text(), 'Hva')]/following-sibling::strong/text()").get()
        event_item['type'] = EventItem.discern_type(type, event_item['name'], event_item['description'])

        start, end = response.xpath(".//time/@datetime").getall()
        if start != None :
            event_item['start'] = datetime.datetime.fromtimestamp(int(start)/1000.0).astimezone(pytz.timezone('Europe/Oslo'))

        if end != None:
            event_item['end'] = datetime.datetime.fromtimestamp(int(end)/1000.0).astimezone(pytz.timezone('Europe/Oslo'))

        event_item['host'] = "Abakus"
        event_item['study_program'] = EventItem.discern_study_program('MTDT, MTKOM', event_item['host'], event_item['description'])

        yield event_item
