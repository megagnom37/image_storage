# Image Storage
 _Test Task_

## Installation

Launch Docker Deamon.
Clone repository to local host machine.

Launch build with Docker Compose:
```sh
docker-compose build
```
Then launch server with DB by Docker Compose:
```sh
docker-compose up
```

## Using
### With interface provided by FastAPI
If settings weren't changed so go to http://0.0.0.0:9999/docs.
Here you can try to work with available test requests.

### With Python CLI client
In this case install all requirements from **requirements.txt**:
```sh
pip install -r /requirements.txt
```
Then you can do different requests via CLI. 
Full list of commands and options available by --help command:
```sh
python cli.py --help
```

## WEB API
WEB API available after running web server by URLs:
 - http://0.0.0.0:9999/docs
 - http://0.0.0.0:9999/redoc

## Server configuration
Server configuration available in Dockerfile in root folder or like env variables.
List of configurating fields:
 - **IST_SERVICE_PORT** - port of service
 - **IST_SERVICE_HOST** - host of service
 - **IST_DB_USER** - DataBase user name
 - **IST_DB_PASSWORD** - DataBase user passeord
 - **IST_DB_HOST** - host name of DataBase service
 - **IST_DB_PORT** - port of DataBase service