import scrapy
import datetime
from ..date_helper import DateHelper
from ..items import Event 
from scrapy.crawler import CrawlerProcess

class EventSpider(scrapy.Spider):
    name = "event"

    def start_requests(self):
        """
        Starts a list of processes for every function-url combo specified
        """

        # Datehelper for use later
        self.date_helper = DateHelper()

        urls = {
            # self.abakus_parse : "https://abakus.no/events",
            self.samfundet_parse : "https://www.samfundet.no/arrangement"
        }

        for yield_func in urls.keys():
            url = urls.get(yield_func)
            yield scrapy.Request(url=url, callback=yield_func)


    def samfundet_parse(self, response):
        """
        Goes to samfundet.no/arrangment and starts another porcess for each event
        """

        for event_element in response.xpath("//td[@class='event-title']/a"):
            url = "https://www.samfundet.no" + event_element.xpath("./@href").get()
            name  = event_element.xpath("./text()").get()
            
            yield scrapy.Request(url=url, callback=self.samfundet_parse_event, cb_kwargs=dict(name=name, url=url))
    
    def samfundet_parse_event(self, response, url, name):
        event = Event()

        event["name"] = name
        event["url"] = url
        event["location"] = response.xpath(".//td[text()='Lokale']/following-sibling::td/a/text()").get()
        event["host"] = "Samfundet"

        norwegian_date = response.xpath(".//td[text()='Dato']/following-sibling::td/text()").get().strip()
        date = self.date_helper.norwegian_month_as_sql_date(norwegian_date)
        hours = response.xpath(".//td[text()='Tid']/following-sibling::td/text()").get()

        hour_start = int(hours[0:2])
        minute_start = int(hours[3:5])
        event["start"] = date.replace(hour=hour_start, minute=minute_start, second=0)

        hour_end = int(hours[-5:-3])
        minute_end = int(hours[-2])
        event["end"] = date.replace(hour=hour_end, minute=minute_end)

        description = ""
        description += response.xpath(".//p[@class='description-short']/text()").get().strip()
        description += "".join(response.xpath(".//div[@class='description-long']/p/text()").getall())
        event["description"] = description

        yield event




    def abakus_parse(self, response):
        """
        Goes to 'abakus.no/events/' and starts another process on each individual events it finds
        """

        for event in response.xpath("//descendant::div[@class='styles__eventItem--2c-Z_4PWb2']"):
            url = "https://Abakus.no" + event.xpath("./div[1]/a/@href").get()
            yield scrapy.Request(url=url, callback=self.abakus_parse_event)

    def abakus_parse_event(self, response):
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

    
if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(EventSpider)
    process.start()