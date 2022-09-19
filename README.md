# Setup an simple OCS using FastAPI, MongoDB and Redis

**Overview**  
This repository simulates a simple Online Charging System with 2 APIs: one for recording call details and one for querying billing information

To speed up the billing info queries, the index for username and caching are used in this application. A process called "event listener" is built to make sure cached data (stored in Redis) is same with data in MongoDB, it leverages the MongoDB Change Stream to listen to the events in DB and update data in Redis.

**Note**  
This setup is for demonstration purposes ONLY.    
Using this setup for local development though, is perfectly fine.  

**Requirements**  
Docker Compose V2  
Docker Engine 19.03.0+

**Usage**  
To run this application, make sure ports 9000, 5500 and 30000 on your local machine are available, then do
```bash
docker compose up --build
```

To run the unit tests, make sure the appplication is up and running, then do
```bash
docker compose exec backend pytest
```

Access localhost:9000/docs for OpenAPI documentation.
