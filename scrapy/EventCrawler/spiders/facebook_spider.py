import scrapy
import datetime
from date_helper import DateHelper
from items import Event 

class FacebookSpider(scrapy.Spider):
    name = "facebook"
    use_selenium = True

    date_helper = DateHelper()

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

        time = response.xpath(".//div[@class='_2ycp _5xhk']/text()").get().split(" – ")
        date = self.date_helper.english_str_as_sql_date(time[0])
        event['start'] = date
        end_hour, end_minute = self.date_helper.hour_str_hour_minute(time[1])
        event['end'] = date.replace(hour=end_hour, minute=end_minute)

        yield event

        
            
