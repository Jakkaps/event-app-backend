import mysql.connector
import os
from event import Event

host = os.environ.get("EVENT_DB_HOST", "localhost")
port = os.environ.get("EVENT_DB_PORT", "3307")
user = "root"
pwd = os.environ.get("EVENT_DB_PWD")
db_name = "event_app"


class EventStorage():
    def __init__(self):
        self.
