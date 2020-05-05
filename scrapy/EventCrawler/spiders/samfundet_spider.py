import scrapy
import datetime
import dateparser
from items import Event 

class SamfundetSpider(scrapy.Spider):
    name = "samfundet"
    start_urls = [
        "https://www.samfundet.no/arrangement"
    ]


    def parse(self, response):
        """
        Goes to samfundet.no/arrangment and starts another porcess for each event
        """

        for event_element in response.xpath("//td[@class='event-title']/a"):
            url = "https://www.samfundet.no" + event_element.xpath("./@href").get()
            name  = event_element.xpath("./text()").get()
            
            yield scrapy.Request(url=url, callback=self.parse_event, cb_kwargs=dict(name=name, url=url))
    
    def parse_event(self, response, url, name):
        event = Event()

        event["name"] = name
        event["url"] = url
        event["location"] = response.xpath(".//td[text()='Lokale']/following-sibling::td/a/text()").get()
        event["host"] = "Samfundet"

        image_style = response.xpath(".//div[@class='banner-image'][1]/@style").get()
        event["image_source"] = "https://samfundet.no" + image_style.split("url(")[1][:-1]

        # The date is one field, and start and end times is one field
        date = dateparser.parse(response.xpath(".//td[text()='Dato']/following-sibling::td/text()").get().strip())
        start, end = response.xpath(".//td[text()='Tid']/following-sibling::td/text()").get().strip().replace('.', ':').split('-')
        start = dateparser.parse(start)
        end = dateparser.parse(end)
        event["start"] = date.replace(hour=start.hour, minute=start.minute)
        event["end"] = date.replace(hour=end.hour, minute=end.minute)

        description = ""
        description += response.xpath(".//p[@class='description-short']/text()").get().strip()
        description += "\n\n".join(response.xpath(".//div[@class='description-long']/p/text()").getall())
        event["description"] = description

        event["type"] = Event.discern_type(None, event["name"], event["description"])

        yield event