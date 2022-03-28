# WIER Programming assignment 1
**Multi-thread broadth-first web crawler Oskar**



## Required libraries for python:
```sh
threading
hashlib
psycopg2
selenium
validator_collection
```



## Database:

Install Docker, pgAdmin and postgresql

- Run command to create database:
```sh
docker run --name postgresql-wier-crawler -e POSTGRES_PASSWORD=SecretPassword -e POSTGRES_USER=crawler -v $PWD/pgdata:/var/lib/postgresql/data -v $PWD/init-scripts:/docker-entrypoint-initdb.d -p 5432:5432 -d postgres:12.2
```
- Run command to start container:
```sh
docker start postgresql-wier-crawler
```
- Run command to log into database:
```sh
docker exec -it postgresql-wier-crawler psql -U crawler
```

*Note: manually added to db:
- crawldb.page column page_hash (Data type: uuid)
- crawldb.site columns ip_address (Data type: inet), crawl_delay (Data type: integer), last_accessed_time (Data type: integer), disallow (Data type: char[])



## Instructions:

- in crawler/thread.py web_driver_location to your path
- in crawler/main.py set number_of_threads to desired number of threads

Run code:
```sh
python main.py
```


