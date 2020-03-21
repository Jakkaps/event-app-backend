from event.app import app
from flask import jsonify
from event.event import Event



@app.route('/get_events')
def get_events():
    """
    Returns a list of all events from all datasources
    """

    # Moch event for testing
    event = Event("AbelLan", "Kult lan for abakuler", "21.03.2020", "Abakus", "A2")
    events = [event.__dict__]
    

    return jsonify(events)
