# Event App Backend 
The backend for finding all interesting events happening for students in Trondheim

## API Documentation
Base url for the API is 
`api.skjerdetno.no`

The API has the following endpoints: 
### /get_events
With no parameters this returns a list of all events in the database.
It is possible to filter these events by passing filter parameters to the query
|Filter Key|Description|Structure|
|---|---|---|
|name|The name of the events you want|String, comma separated for several values|
|class_year|A number describing which class years are allowed at the event|Number, comma separated for more values|
|host|The name of the event host| String, comma separated for more values|
|study_program|Names of all study programs allowed at the event| String, comma separated for more values|
|start|The first date any returned event should be on|Date string on the format YYYY-MM-DD|
|end|The last date any returned event should be on|Date string on the format YYYY-MM-DD|

Each parameter is given as normal url paramters like `/get_events?key=value&other_key=other_value`

**An example query**: 
```/get_events?host=Abakus,Samfundet&type=Fest&start=2020-05-02&class_year=1```

### /search?query=
You must pass the `?query` parameter to this endpoint. Returnes all events matching this query, sorted by relevance

### /get_hosts
Returns a list of all hosts of events that skjerdet.no knows about
Takes no paramters

### /get_types
Returns a list of all event types that skjerdet.no knows about
Takes no paramters

## Running 
To run the project properly you need the following environment variable:
- `EVENT_DB_PWD`

### Production 
To start the application run 
```bash
$ docker-compose up -d --build
```
Optionaly for debuggin (until logging is in place) you can drop the `-d` flag to view any output

To stop it run 
```bash
$ docker-compose down
```

### Local development
#### Flask app
NB: the database must be running! 
```bash
$ cd flask 
$ export FLASK_APP=event.app
$ export FLASK_ENV=development
$ flask run 
```

#### Database
If the production app is not running, in the root dir of the project run 

```bash 
$ docker-compose run -p 3306:3307 event_db
```


To then stop it run 
```bash 
$ docker-compose down 
```

#### Spiders
To run the spiders, do

```bash
$ python scrapy/EventCrawler/run_spiders.py
```
Given that the database is running, this will write all events to database.

