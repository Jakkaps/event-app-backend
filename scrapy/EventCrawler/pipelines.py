# -*- coding: utf-8 -*-

# Define your item pipelines here

from .items import Event

class EventcrawlerPipeline(object):
    def process_item(self, event : Event, spider):
        """
        Update the database with an event. This method is called after every event the spider finds.
        """

        # TODO: Standarize event type 
        print(event['name'])
        return event
