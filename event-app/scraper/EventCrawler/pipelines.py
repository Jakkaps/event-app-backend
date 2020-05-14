# -*- coding: utf-8 -*-

# Define your item pipelines here

from scraper.EventCrawler.items import EventItem
from event import EventStorage
import os
import mysql.connector

class EventcrawlerPipeline(object):
    def open_spider(self, item):
        """
        Called when the spider opens. Connects to the given database and stores the connection 
        """
        self.event_storage = EventStorage()

    def close_spider(self, spider):
        """
        Called when the spider closes. Closes the connection to the database
        """

    def process_item(self, event_item:EventItem, spider):
        """
        Update the database with an event. This method is called after every event the spider finds.
        """

        self.event_storage.add_or_update_event(event_item.__dict__)


        return event_item
    
     
