import mysql.connector
import os
from elasticsearch import Elasticsearch
from event import Event
from event import EventFilter

import logging

host = os.environ.get("EVENT_DB_HOST", "localhost")
port = os.environ.get("EVENT_DB_PORT", "3307")
user = "root"
pwd = os.environ.get("EVENT_DB_PWD")
db_name = "event_app"

es_host = os.environ.get("ELASTIC_HOST", "localhost")


class EventStorage():

    def connect_es(self):
        logging.debug("GOING TO CONNECT TO ES ON HOST: " + es_host)
        self.es = Elasticsearch([{"host": es_host}])
        self.index_name = "events"
    
    def connect_db(self):
        """Connects to the database
        Used internally"""
        self.db = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=pwd,
            database=db_name,
            auth_plugin='mysql_native_password'
        )

    def set_es_mapping(self):
        """
        Makes sure the index has the right mapping with correct analyzers
        """
        self.connect_es()
        mapping_data = {
            "settings": {
                "analysis": {
                    "filter": {
                        "autocomplete_filter": {
                            "type": "edge_ngram",
                            "min_gram": 1,
                            "max_gram": 20
                        }
                    },
                    "analyzer": {
                        "autocomplete": { 
                            "type": "custom",
                            "tokenizer": "standard",
                            "filter": [
                                "lowercase",
                                "autocomplete_filter"
                            ]
                        }
                    }
                }
            },
            "mappings": {
                "_doc": {
                    "properties": {
                        "name": {
                            "type": "text",
                            "analyzer": "autocomplete", 
                            "search_analyzer": "standard" 
                        },
                        "host": {
                            "type": "text",
                            "analyzer": "autocomplete", 
                            "search_analyzer": "standard" 
                        },
                        "description": {
                            "type": "text",
                            "analyzer": "autocomplete", 
                            "search_analyzer": "standard" 
                        },
                        "type": {
                            "type": "keyword",
                            "analyzer": "autocomplete", 
                            "search_analyzer": "standard" 
                        }
                    }
                }
            }
        }

        self.es.index(index="evets", body=mapping_data)


    def get_all_events(self) -> [Event]:
        """Returns a list of all stored events"""
        self.connect_db()
        query = "SELECT * FROM events"

        cursor = self.db.cursor()
        cursor.execute(query)

        events = []
        for e in cursor:
            e = e[1:]
            event = Event(*e)
            events.append(event)
        cursor.close()

        self.db.close()

        return events

    def get_filtered_events(self, filters: [EventFilter]=[]) -> [Event]:
        """
        Returns a list of all events matching the filters given
        """
        self.connect_db()

        query = "SELECT * FROM events"

        filter_values = [f.values for f in filters]

        # A bit strange expression, but this should flatten the
        # list of lists of filtervalues
        query_filters_values = [y for x in filter_values for y in x]
        print(query_filters_values)
        if len(filters) != 0:
            query += " WHERE "

            # We must separate the query filter and the actual value
            # to prevent SQL injection
            query_filters = []

            for f in filters:
                filter_variations = []
                for v in f.values:
                    # Each filter key can have multiple values to check against
                    # These should be joined by OR and surrounded by parentheses
                    filter_variations.append(f"{f.key} {f.operator} ?")
                query_filters.append(f"({' OR '.join(filter_variations)})")

            query += " AND ".join(query_filters)

        query += ";"


        print(query)
        cursor = self.db.cursor(prepared=True)
        cursor.execute(query, query_filters_values)

        events = []
        for e in cursor:
            e = e[1:]
            event = Event(*e)
            events.append(event)
        cursor.close()

        self.db.close()

        return events

    def get_all_hosts(self) -> [str]:
        """
        returns a list of all hosts in the database
        """
        self.connect_db()
       
        query = "SELECT DISTINCT host from events"

        cursor = self.db.cursor()
        cursor.execute(query)

        hosts = []

        for host in cursor:
            sub_hosts = host[0].split("")
            for sub_host in sub_hosts:
                hosts.append(sub_host)

        self.db.close()
        return list(set(hosts)) #This makes sure values are unique

    def get_all_types(self) -> [str]:
        """Returns a list of all unique types from the database"""

        self.connect_db()
        query = "SELECT DISTINCT type FROM events"
        cursor = self.db.cursor()
        cursor.execute(query)

        types = [t[0] for t in cursor]

        self.db.close()
        return types

    def get_all_study_programs(self) -> [str]:
        """
        Returns a list of all study programs mensioned in events in the db
        """
        self.connect_db()
        query = "SELECT DISTINCT study_program FROM events"
        cursor = self.db.cursor()
        cursor.execute(query)

        study_programs = []
        for sp in cursor:
            if sp[0] != None: 
                programs = sp[0].split(",")
                for program in programs:
                    study_programs.append(program)
            

        self.db.close()
        return list(set(study_programs)) #This makes sure values are unique


    def search(self, query: str):
        self.connect_es()
        self.connect_db()
        search_result = self.es.search(index="events", body={
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["*"],
                    "fuzziness": "AUTO",
                }
            }
        })["hits"]["hits"];

        events = []

        for result in search_result:
            cursor = self.db.cursor()
            sql_query = f"SELECT * FROM events WHERE id = {result['_id']}"
            cursor.execute(sql_query)
            for e in cursor:
                e = e[1:]
                event = Event(*e)
                events.append(event)
            cursor.close()

        self.db.close()
        return events
                

    def getSuggestions(self, query):
        """
        Returns a list of suggestions for what the user might want to search on
        based on the query and tha data we have indexed
        """
        return []




    def get_event_id(self, event: Event) -> str:
        """
        Returns the ID of a given event from the database
        """
        self.connect_db()
        cursor = self.db.cursor()

        query = f"SELECT id FROM events WHERE name = '{event.name}' AND host = '{event.host}'"
        cursor.execute(query)
        result = ""
        for res in cursor:
            result = res[0]
        cursor.close()
        self.db.close()
        return result


    def add_or_update_event(self, event: dict):
        """
        Adds the given event dictionary to the database, and the elasticsearch index

        If the event is already there it will update
        """
        self.connect_db()
        self.connect_es()
        
        cursor = self.db.cursor(buffered=True)

        
        # Inserting into the database
        query = "INSERT INTO events ("
        keys = list(event.keys())
        for key in keys:
            query += f"{key}, "
        query = query[:-2] + ") "

        query += "VALUES("
        for key in keys:
            query += f"'{event[key]}', "
        query = query[:-2] + ") "

        query += "ON DUPLICATE KEY UPDATE "
        for key in keys:
            query += f"{key}='{event[key]}', "
        query = query[:-2].replace("None", "NULL")

            
        cursor.execute(query)
        cursor.close()
        self.db.commit()
        self.db.close()

        # Adding to elasticsearch
        id = self.get_event_id(Event(**event))

        index_body = {
            "name": event['name'],
            "host": event['host'],
            "description": event['description'],
            "type": event['type'],
        }


        self.es.index(index=self.index_name, id=id, refresh=True, body=index_body)

