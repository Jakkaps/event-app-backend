import scrapy
import datetime
from date_helper import DateHelper
from items import Event 

class SamfundetSpider(scrapy.Spider):
    name = "samfundet"
    start_urls = [
        "https://www.samfundet.no/arrangement"
    ]

    date_helper = DateHelper()

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

        event["type"] = Event.discern_type(None, event["name"], event["description"])

        yield event