from flask import Flask
from event.database.database_handler import DatabaseHandler
import os

app = Flask(__name__)

db_host = os.environ.get("EVENT_DB_HOST", "localhost")
db_port = os.environ.get("EVENT_DB_PORT", "3307")
db_user = "root"
db_pwd = os.environ.get("EVENT_DB_PWD")


database_handler = DatabaseHandler(db_host, db_port, db_user, db_pwd)

import event.endpoints
