from flask import Flask
from event.database.database_handler import DatabaseHandler
import os

db_host = os.environ.get("EVENT_DB_HOST", "localhost")
db_port = os.environ.get("EVENT_DB_PORT", "3307")
db_user = "root"
db_pwd = os.environ.get("EVENT_DB_PWD")

app = Flask(__name__)
database_handler = DatabaseHandler("localhost", 3307, "root", "password")

import event.endpoints
