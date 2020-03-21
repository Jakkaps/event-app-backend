from flask import Flask
from event.database.database_handler import DatabaseHandler
app = Flask(__name__)

import event.endpoints
