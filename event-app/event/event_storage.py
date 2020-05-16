import mysql.connector
import os
from event import Event
from event import EventFilter

host = os.environ.get("EVENT_DB_HOST", "localhost")
port = os.environ.get("EVENT_DB_PORT", "3307")
user = "root"
pwd = os.environ.get("EVENT_DB_PWD")
db_name = "event_app"


class EventStorage():
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
            hosts.append(host[0])
        self.db.close()
        return hosts

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
                programs = sp[0].split(", ")
                for program in programs:
                    study_programs.append(program)
            

        self.db.close()
        return study_programs


    def search(self, search_string):
        """
        Returns all events where the string matches either the
        - name
        - host
        - location
        - description
        - type
        """

        query = """SELECT * FROM events WHERE
        name LIKE ?
        OR host LIKE ?
        OR description LIKE ?
        OR location LIKE ?
        OR type LIKE ?"""

        test = "SELECT * FROM events WHERE name = %s"

        self.connect_db()
        cursor = self.db.cursor(prepared=True)
        cursor.execute(query, [f"%{search_string}%" for i in range(5)])
        # cursor.execute(test, (search_string,))
        events = []
        for e in cursor:
            print(e)
            e = list(e[1:])
            event = Event(*e)
            events.append(event)
        cursor.close()

        self.db.close()
       
        return events

    def add_or_update_event(event: dict):
        self.connect_db()

        
        cursor = self.db.cursor()
        
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
        
        



