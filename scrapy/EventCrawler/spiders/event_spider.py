import scrapy
from ..items import Event 

class EventSpider(scrapy.Spider):
    name = "event"

    def start_requests(self):
        """
        Starts a list of processes for every function-url combo specified
        """
        urls = {
            self.abakus_parse : "https://Abakus.no/events"
        }

        for yield_func in urls.keys():
            url = urls.get(yield_func)
            yield scrapy.Request(url=url, callback=yield_func)

    
    def abakus_parse(self, response):
        """
        Goes to 'Abakus.no/events/' and starts another process on each individual events it finds
        """
        
        events = []
        print(response)

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
        start = response.xpath("/html/body/div/div/div/div[2]/div/div/div[2]/div[1]/div[2]/ul/li[span[contains(text(), 'Når')]]/strong/span/time/@datetime").get()
        location = response.xpath("/html/body/div/div/div/div[2]/div/div/div[2]/div[1]/div[2]/ul/li[span[contains(text(), 'Finner sted')]]/strong/text()").get()

        description = ""
        for paragraph in response.xpath("/descendant::span[@data-text='true']/text()"):
            description += paragraph.get() + "\n"
        description = description[:-2]

        study_program = "MTDT, MTKOM"
        host = "Abakus"

        yield Event(name=name, description=description, url=url, host=host, start=start, location=location, type=type, study_program=study_program)