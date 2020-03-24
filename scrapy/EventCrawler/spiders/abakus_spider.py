import scrapy
import datetime
from date_helper import DateHelper
from items import Event 
from scrapy.crawler import CrawlerProcess

class AbakusSpider(scrapy.Spider):
    name = "abakus"
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
                
        url = response.request.url
        name = response.xpath("/html/body/div/div/div/div[2]/div/div/div[2]/h2/text()").get()
        type = response.xpath("/html/body/div/div/div/div[2]/div/div/div[2]/div[1]/div[2]/ul/li[span[contains(text(), 'Hva')]]/strong/text()").get()
        location = response.xpath("/html/body/div/div/div/div[2]/div/div/div[2]/div[1]/div[2]/ul/li[span[contains(text(), 'Finner sted')]]/strong/text()").get()

        start_as_milli = int(response.xpath("/html/body/div/div/div/div[2]/div/div/div[2]/div[1]/div[2]/ul/li[span[contains(text(), 'Når')]]/strong/span/time/@datetime").get())
        start_as_date = datetime.datetime.fromtimestamp(start_as_milli/1000.0)
        start = start_as_date.strftime('%Y-%m-%d %H:%M:%S')

        description = ""
        for paragraph in response.xpath("/descendant::span[@data-text='true']/text()"):
            description += paragraph.get().replace("\n", "").replace("'", "")
        description = "".join(description)

        study_program = "MTDT, MTKOM"
        host = "Abakus"

        yield Event(name=name, description=description, url=url, host=host, start=start, location=location, type=type, study_program=study_program)