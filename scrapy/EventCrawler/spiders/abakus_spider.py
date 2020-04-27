import scrapy
import datetime
from date_helper import DateHelper
from items import Event 
from scrapy.crawler import CrawlerProcess

class AbakusSpider(scrapy.Spider):
    name = "abakus"
    use_selenium = True
    start_urls = [
        "https://abakus.no/events",
    ]

    date_helper = DateHelper()

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
        
        event = Event()
                
        event['url'] = response.request.url
        event['name'] = response.xpath(".//h2[@class='ContentHeader__header--2o7lNZxfWI EventDetail__title--13hgFeanVH']/text()").get()
        event['location'] = response.xpath(".//span[contains(text(), 'Finner sted i')]/following-sibling::strong/text()").get()
        event['image_source'] = response.xpath(".//div[@class='Content__cover--26DXPSf5Zo utilities__contentContainer--3A4ds4UtSA utilities__container--2q0U2oWNNe']/img/@src").get()

        description = ""
        for paragraph in response.xpath("//span[@data-text='true']/text()"):
             description += paragraph.get().replace("\n", "").replace("'", "")
        event['description'] = "".join(description)

        type = response.xpath(".//span[contains(text(), 'Hva')]/following-sibling::strong/text()").get()
        event['type'] = Event.discern_type(type, event['name'], event['description'])

        datetime = response.xpath(".//time[1]/@datetime").get()
        if datetime != None :
            start_as_milli = int(datetime)
            event['start'] = self.date_helper.milli_as_sql_date(start_as_milli)

        event['study_program'] = "MTDT, MTKOM"
        event['host'] = "Abakus"

        yield event