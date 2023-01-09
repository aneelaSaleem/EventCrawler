## Lucerne Festival Events Crawler
### Future Demand coding challenge

This project crawls summer festival events from [Lucerne Festival](!https://www.lucernefestival.ch/en/program/summer-festival-23) and save into postgress db.

### How to run?

#### From local machine
It's very simple to run from local machine. I tested it on mac. I hope it works on other operating systems too. 
You have to follow these steps:
1. Setup environment using `make setup` command
2. activate virtual environment `source venv/bin/activate`
3. Check python style using `make lint`
4. Run tests python `make test`
5. Execute program `make run`
6. Deactivate virtual environment `deactivate`
7. Clean virtual environment `make clean`

#### With docker
1. You need to have docker and docker-compose installed on your system and docker process should be running
2. Run `docker-compose up`, it will create containers using postgress credentials from .env file
3. It will run, crawl events and store in the table `events` in `coding_challenge` db.
4. To verify 
    - run `docker ps` and note container_id
    - run docker exec -it {container_id} bash
    - psql postgres://aneela:aneela123@localhost:5432/coding_challenge (change user/password if you modify .enf file)
    - \d will display tables inside db
    - run queries like `select count(*) from events;`
5. shutdown containers `docker-compose down`

### Output screenshots
![Alt text](./images/test-cases.png?raw=true "Test Cases")

------------------------
![Alt text](./images/docker-screenshot.png?raw=true "docker")

------------------------
![Alt text](./images/table-screenshot-inside-docker.png?raw=true "Table in Docker")