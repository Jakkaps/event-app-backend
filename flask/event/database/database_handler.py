import mysql.connector
from event.event import Event

class DatabaseHandler(object):
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def connect(self):
        """
        Connects to the given database and stores the connection 
        """

        self.db = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database="event_app",
            auth_plugin='mysql_native_password'
        )
        
    def get_all_events(self, filters=None) -> [Event]:
        """
        Returns all events in database, that matches the filters given.
        The filter should be given as a dictionary with column_name: value
        """
        self.connect()

        query = "SELECT * FROM events"

        # Find all the nonempty values that should be filtered for
        filter_values = [value for value in filters.values() if value != ""]

        # If any filters applicable add them to the query
        if len(filter_values) != 0:
            query += " WHERE "
            query += " AND ".join([f"{key} LIKE ?" for key in filters if filters[key] != ""])

        cursor = self.db.cursor(prepared=True)
        cursor.execute(query, filter_values)

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
        self.connect()
       
        query = "SELECT DISTINCT host from events"

        cursor = self.db.cursor()
        cursor.execute(query)

        hosts = []

        for host in cursor:
            hosts.append(host[0])
        self.db.close()
        return hosts

    def search(self, search_string) -> [Event]:
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
