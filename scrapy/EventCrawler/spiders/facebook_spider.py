import scrapy
import datetime
from items import Event
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

        for event_url in response.xpath(".//a[@data-hovercard]/@href").getall():
            # Check if the url is actually an event url
            if 'events' not in event_url:
                continue
            
            url = "https://facebook.com" + event_url
            yield scrapy.Request(url=url, callback=self.parse_event, cb_kwargs=dict(study_program=study_program)) 

    
    def parse_event(self, response, study_program):
        event = Event()
 
        event['name'] = response.xpath(".//h1[@data-testid='event-permalink-event-name']/text()").get()
        event['description'] = '\n'.join(response.xpath(".//div[@class='_63ew']/span/text()").getall())
        event['host'] = response.xpath(".//div[@data-testid='event_permalink_feature_line']/@content").get()
        event['location'] = response.xpath(".//span[@class='_5xhk']/text()").get()
        event['url'] = response.request.url 
        event['study_program'] = study_program
        event['image_source'] = response.xpath(".//div[@class='uiScaledImageContainer _3ojl']/img/@src").get()

        event['type'] = Event.discern_type(None, event['name'], event['description'])

        # Get's two dates, one with the full start and one with only the hours of the end
        date = response.xpath(".//div[@class='_2ycp _5xhk']/text()").get()
        logging.debug('THIS WAS THE DATE FOR THE FACEBOOK EVENT: ' + date)
        if 'from' not in date:
            start, end = date.replace('–', '-').split('-') # Replace weird virgin – with chad -
            logging.debug('START ' + start + ' END ' + end)
            start = dateparser.parse(date)
            event['start'] = start
            end = dateparser.parse(end)
            end = start.replace(hour=end.hour, minute=end.minute)
            event['end'] = end
        else:
            date, hours = date.split(' from ')
            start, end = hours.split('-')

            date = dateparser.parse(date)
            start = dateparser.parse(start)
            end = dateparser.parse(end)

            event['start'] = date.replace(hour=start.hour, minute=start.minute)
            event['end'] = date.replace(hour=end.hour, minute=end.minute)

        yield event

        
            
