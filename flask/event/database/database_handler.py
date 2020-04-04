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

        self.connect()
        query = "SELECT * FROM events"

        # Adding the filter clause to the query
        FILTER = ""
        if not filters is None and bool(filters):
            FILTER = " WHERE "
            for f in filters:
                if filters[f] != "":
                    FILTER += f"{f}={filters[f]}"

        query += FILTER

        cursor = self.db.cursor(dictionary=True)

        cursor.execute(query)


        events = []
        for e in cursor:
            del e["id"]
            event = Event(**e)
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
