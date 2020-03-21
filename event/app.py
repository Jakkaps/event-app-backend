from flask import Flask
from event.database.database_handler import DatabaseHandler
app = Flask(__name__)

handler = DatabaseHandler("localhost", 3307, "root", "password")

@app.route('/')
def hello_world():
    """Print 'Hello, world!' as the response body."""
    return 'Hello, world!'

