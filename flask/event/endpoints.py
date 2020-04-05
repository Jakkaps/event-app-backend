from event.app import app, database_handler
from flask import jsonify, request
from event.event import Event


@app.route('/get_events')
def get_events():
    """
    Returns a list of all events from all datasources
    
    It is possible to filter the request with the following flags
    - name: str – name containing the given string 
    - class_year: str – study program containing given string
    - host: str – Name of the host
    - study_program: str – name of the study programs allowed
    - start: str (timestamp) – The earliest starting time of the events
    - Soon: dateRange: str – two timestamps separated with - as 'start-stop'.
    Gives all events in the interval
    - 
    """

    # Handle the filters
    filters = {}

    for key in request.args:
        filters[key] = request.args[key]


    # filter the list of events based on the query
    # Temporary filter for now... this should be done in the query
    events = database_handler.get_all_events(filters)
    events = [e.__dict__ for e in events]

    
    return jsonify(events)


@app.route('/search')
def search():
    """
    Search the event database for the given query 
    """
    query = request.args.get('query')

    # Execute the query
    events = [e.__dict__ for e in database_handler.search(query)]

    return jsonify(events)
    
@app.route('/get_hosts')
def get_hosts():
    """
    Returns a list of all hosts with events in the database
    """
    hosts = database_handler.get_all_hosts()
    print(hosts)
    return jsonify(hosts)
