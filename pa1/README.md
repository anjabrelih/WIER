# WIER Programming assignment 1
Multi-thread broadth-first web crawler Oskar

*Required libraries for python:
threading
hashlib
psycopg2
selenium
...

*Database:
Install Docker, pgAdmin and postgresql

Run command to create database:
docker run --name postgresql-wier-crawler -e POSTGRES_PASSWORD=SecretPassword -e POSTGRES_USER=crawler -v $PWD/pgdata:/var/lib/postgresql/data -v $PWD/init-scripts:/docker-entrypoint-initdb.d -p 5432:5432 -d postgres:12.2

Run command to start container:
docker start postgresql-wier-crawler

Run command to log into database:
docker exec -it postgresql-wier-crawler psql -U crawler

Note: manually added to db:
- crawldb.page column page_hash (Data type: uuid)
- crawldb.site columns ip_address (Data type: inet), last_accessed_time (Data type: timestamp without time zone) and crawl_delay (Data type: integer)



*Instructions:

in crawler/crawler.py web_driver_location to your path
in crawler/main.py set number_of_threads to desired number of threads

Run code:
python main.py


