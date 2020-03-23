# -*- coding: utf-8 -*-

# Define your item pipelines here

from .items import Event
import os
import mysql.connector

class EventcrawlerPipeline(object):
    def open_spider(self, item):
        """
        Called when the spider opens. Connects to the given database and stores the connection 
        """

        password = os.environ['EVENT_DB_PWD']
        self.db = mysql.connector.connect(
            host="localhost",
            port=3307,
            user="root",
            password=password,
            database="event_app",
            auth_plugin='mysql_native_password'
        )


        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        """
        Called when the spider closes. Closes the connection to the database
        """
        self.db.commit()
        self.cursor.close() 


    def process_item(self, event:Event, spider):
        """
        Update the database with an event. This method is called after every event the spider finds.
        """
        
        query = "INSERT INTO events ("
        for key in event.keys():
            query += f"{key}, "
        query = query[:-2] + ") "

        query += "VALUES("
        for key in event.keys():
            query += f"'{event[key]}', "
        query = query[:-2] + ") "

        query += "ON DUPLICATE KEY UPDATE "
        for key in event.keys():
            query += f"{key}='{event[key]}', "
        query = query[:-2].replace("None", "NULL")
            
        self.cursor.execute(query)

        # TODO: Standarize event type 

        return event
    
     
