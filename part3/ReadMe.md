# Part 3

Sample FLASK app to serve officer data through an API to a technical audience.


## Running the app

Requires: `docker` & `docker-compose` to be installed on your machine.

**Using `docker-compose`**  *(from the root of the repository):*

```
cd ./part3

docker-compose build 

docker-compose up
```
To stop the container use `ctrl+c`


**Alternatively using `docker run`**  *(from the root of the repository):*

```
cd ./part3

docker build -t cma_officers .          

docker run -it --name cma_officers-api -p 0.0.0.0:8000:8000/tcp cma_officers
```


## App usage and API endpoints

[http://localhost:8000](http://localhost:8000) - landing page

[http://localhost:8000/company](http://localhost:8000/company) - list of unique company numbers

[http://localhost:8000/company/<company_number>](http://localhost:8000/company/88958775) - officers from a single commpany

[http://localhost:8000/country](http://localhost:8000/country) - list of unique countries

[http://localhost:8000/country/<country>](http://localhost:8000/country/SCOTLAND) - officcers from a single country


## Future improvements

### Flask API improvements

There are many ways to extend this API, more endpoints and more advanced ways to query the data.  Several options:

- include filtering of multiple attributes at the same time, probably easiest to use parameters in the GET URL and parse these.  I decided to use object endpoints to demonstrate something more Restful.
- limit responses to a capped amount, include a GET parameter to page through results. This would prevent too much data being returned when the dataset grows


### Container improvements

For a production implementation the following container changes are recommended at a minimum:

- Reverse Proxy Web Server - The container already uses produciton WSGI server (Waitress), however this would be better to be reverse-proxied through a Web Server such as NGINX or Apache.  It would be  simple to add another container to the docker-compose file and reverse proxy through this.  

- Database rather than in-memory store.  Any production implementation of this needs a better data source to improve performance.  I suggest a database such as Postgres as DB queries could handle much bigger datasets through use of indicess.  This could be implemented using an additional container with mounted volume, but would require a simple ETL script to load the input CSV into it on first instatiation.  Alternatively a separate DB server could be used which could be hosted on the cloud or private server.
