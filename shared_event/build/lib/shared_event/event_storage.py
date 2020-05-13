import mysql.connector
import os
from event import Event
from EventFilter import EventFilter

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
            password=password,
            database=db_name,
            auth_plugin='mysql_native_password'
        )

    def get_all_events(self) -> [Event]:
        """Returns a list of all stored events"""
        self.connect()
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
        self.connect()

        query = "SELECT * FROM events"

        filter_values = []
        if len(filters) != 0:
            query += " WHERE "

            # We must separate the query filter and the actual value
            # to prevent SQL injection
            query_filters = [f"{filter.key} {filter.operator} ?" for filter in filters]
            query_filters_values = [filter.value for filter in filters]

            query += " AND ".join(query_filters)


        cursor = self.db.cursor(prepared=True)
        cursor.execute(query, query_filter_values)

        events = []
        for e in cursor:
            print(e)
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
        self.connect()
       
        query = "SELECT DISTINCT host from events"

        cursor = self.db.cursor()
        cursor.execute(query)

        hosts = []

        for host in cursor:
            hosts.append(host[0])
        self.db.close()
        return hosts

    def search(self):
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

        self.connect()
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



