from event.app import app, database_handler
from flask import jsonify, request
from event.event import Event


@app.route('/get_events')
def get_events():
    """
    Returns a list of all events from all datasources
    
    It is possible to filter the request with the following flags
    - name: str – name containing the given string 
    - studyProgram: str – study program containing given string
    - dateRange: str – two timestamps separated with - as 'start-stop'. 
    Gives all events in the interval
    - 
    """

    # Handle the filters
    name = request.args.get("name", "") 
    studyProgram = request.args.get("studyProgram", "")
    dateRangeStr = request.args.get("dateRange", "")


    # Moch event for testing
    event = Event("AbelLan", "Kult lan for abakuler", "21.03.2020", "Abakus", "A2")

    # filter the list of events based on the query
    # Temporary filter for now... this should be done in the query
    events = database_handler.get_all_events()
    events = [e.__dict__ for e in events if (name in e.name)]

    
    return jsonify(events)


@app.route('/search')
def search():
    """
    Search the event database for the given query 
    """
    query = request.args.get('query')

    # Execute the query
    
@app.route("/random")
def random():
    return "random"
