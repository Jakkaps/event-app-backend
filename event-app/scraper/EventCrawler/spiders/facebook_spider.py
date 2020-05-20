import scrapy
import datetime
from scraper.EventCrawler.items import EventItem
import dateparser 
import logging

class FacebookSpider(scrapy.Spider):
    name = "facebook"
    use_selenium = True

    def start_requests(self):
        fb_pages = {
            "Energi og Miljø" : "https://www.facebook.com/pg/emilface/events/"
        }
    
        for study_program in fb_pages.keys():
            url = fb_pages.get(study_program)
            yield scrapy.Request(url=url, callback=self.parse_events_page, cb_kwargs=dict(study_program=study_program))



    def parse_events_page(self, response, study_program):
        """
        Creates a subproccess for each event in a facebook events-page
        """

        event_urls = response.xpath(".//a[@data-hovercard]/@href").getall()
        logging.info(f"ALL FACEBOOK URLS: {event_urls}")
        for event_url in event_urls:
            # Check if the url is actually an event url
            if 'events' not in event_url:
                continue
            
            url = "https://facebook.com" + event_url
            yield scrapy.Request(url=url, callback=self.parse_event, cb_kwargs=dict(study_program=study_program)) 

    
    def parse_event(self, response, study_program):
        event_item = EventItem()
 
        event_item['name'] = response.xpath(".//h1[@data-testid='event-permalink-event-name']/text()").get()
        event_item['description'] = '\n'.join(response.xpath(".//div[@class='_63ew']/span/text()").getall())
        event_item['host'] = EventItem.discern_host(response.xpath(".//div[@data-testid='event_permalink_feature_line']/@content").get())
        event_item['location'] = response.xpath(".//span[@class='_5xhk']/text()").get()
        event_item['url'] = response.request.url 
        event_item['study_program'] = EventItem.discern_study_program(study_program, event_item['host'], event_item['description'])
        event_item['image_source'] = response.xpath(".//div[@class='uiScaledImageContainer _3ojl']/img/@src").get()

        event_item['type'] = EventItem.discern_type(None, event_item['name'], event_item['description'])

        # Get's two dates, one with the full start and one with only the hours of the end
        date = response.xpath(".//div[@class='_2ycp _5xhk']/text()").get()
        if 'from' in date:
            date, hours = date.split(' from ')
        else:
            date, hours = date.split(' at ')
        
        hours = hours.replace('–', '-')
        start, end = hours.split('-')
        date = dateparser.parse(date)
        start = dateparser.parse(start)
        end = dateparser.parse(end)

        event_item['start'] = date.replace(hour=start.hour, minute=start.minute)
        event_item['end'] = date.replace(hour=end.hour, minute=end.minute)

        yield event_item 

        
            
