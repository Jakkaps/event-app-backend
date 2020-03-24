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
        print(self.host, self.port, self.user, self.password)
        self.db = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database="event_app",
            auth_plugin='mysql_native_password'
        )

    def set_events(self, events: [Event]):
        """
        Takes a list of events and updates the database to reflect the list
        
        If an event in the list is already in the database it will be altered, 
        if not it will be added
        """

        self.connect()

        db_event_names = [e.name for e in self.get_all_events()]

        for event in events:
            if event.name in db_event_names:
                # The event with this name is already in the database
                self.update_event(event)
            else:
                # this is a new event
                self.add_event(event)

        self.db.close()
            

        
    def get_all_events(self) -> [Event]:
        print("connecting")
        self.connect()
        query = "SELECT * FROM events"
        print("going to query the db")
        cursor = self.db.cursor(dictionary=True)
        print("got the cursor")
        cursor.execute(query)
        print("executed")


        events = []
        for e in cursor:
            del e["id"]
            event = Event(**e)
            events.append(event)
        cursor.close()

        self.db.close()

        return events
    

    def add_event(self, event: Event):
        query = f"""INSERT INTO events (name, description, start, end, host, location, url, study_program, class_year) 
        VALUES 
        {event.name, event.description, event.start, event.end, event.host, event.location, event.url, event.type, event.study_program, event.class_year}"""

        # for key in event.__dict__:
        #     query += f"{key}='{event.__dict__[key]}, "

        query = query.replace("None", "NULL")

        cursor = self.db.cursor()
        cursor.execute(query)
        self.db.commit()
        cursor.close()

    def update_event(self, event: Event):
        query = "UPDATE events SET "
        for key in event.__dict__:
            query += f"{key}='{event.__dict__[key]}', "

        
        query = query[:-2].replace("'None'", "NULL")
        query += f" WHERE name='{event.name}' AND host={event.host}"
            
        cursor = self.db.cursor()
        cursor.execute(query)
        self.db.commit()
        cursor.close()
        
       
    

    
