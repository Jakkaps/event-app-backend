# Event App Backend 
The backend for finding all interesting events happening for students in Trondheim

## Running 
### Database
The database is a MySQL database running with docker
To build the database locally do

```bash
cd mysql
```

```bash 
./build_database.sh` or `docker build -t event_db .
```

Then, to run: 

```bash
./run_database
```

If you need to rebuild the database, run the build script then
```bash
docker stop event_db
```

```bash
docker ps -a
``` 
and find the id of the event_db container

```bash
docker rm <ID of your container>
```
Then run the start database script
