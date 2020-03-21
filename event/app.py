from flask import Flask
from event.database.database_handler import DatabaseHandler
app = Flask(__name__)
database_handler = DatabaseHandler("localhost", 3307, "root", "password")
import event.endpoints
