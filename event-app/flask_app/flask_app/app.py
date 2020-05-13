from flask import Flask
from flask_cors import CORS
from event import EventStorage
import os

from event.event_storage import EventStorage

app = Flask(__name__)
CORS(app)

event_storage = EventStorage()

import flask_app.flask_app.endpoints 
