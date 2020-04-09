# Event App Backend 
The backend for finding all interesting events happening for students in Trondheim

## Endpoints



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

