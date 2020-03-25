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

        self.db_password = os.environ['EVENT_DB_PWD']
        self.db_host = os.environ['EVENT_DB_HOST', "localhost"]
        self.db_port = os.environ['EVENT_DB_PORT', "3307"]
        db_user = "root"
        self.db = mysql.connector.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database="event_app",
            auth_plugin='mysql_native_password'
        )



    def close_spider(self, spider):
        """
        Called when the spider closes. Closes the connection to the database
        """
        self.db.commit()
        self.db.close()

    def process_item(self, event:Event, spider):
        """
        Update the database with an event. This method is called after every event the spider finds.
        """

        cursor = self.db.cursor()
        
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
            
        cursor.execute(query)
        cursor.close()
        self.db.commit()


        # TODO: Standarize event type 

        return event
    
     
