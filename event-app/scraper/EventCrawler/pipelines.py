# -*- coding: utf-8 -*-

# Define your item pipelines here

from scraper.EventCrawler.items import EventItem
from event import EventStorage
import os
import mysql.connector
import logging

logger = logging.getLogger()

class EventcrawlerPipeline(object):
    def open_spider(self, item):
        """
        Called when the spider opens. 
        """
        self.event_storage = EventStorage()
        self.event_storage.set_es_mapping()

    def close_spider(self, spider):
        """
        Called when the spider closes. 
        """
        pass

    def process_item(self, event_item:EventItem, spider):
        """
        Update the database with an event. This method is called after every event the spider finds.
        """

        self.event_storage.add_or_update_event(event_item.__dict__['_values'])

        return event_item
    
     
