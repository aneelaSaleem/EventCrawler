import logging
import os
import json
import psycopg2
from dotenv import load_dotenv

load_dotenv()
logging.getLogger().setLevel(logging.INFO)


def get_connection_string_from_env():
    user = os.environ['POSTGRES_USER']
    password = os.environ['POSTGRES_PASSWORD']
    db = os.environ['POSTGRES_DB']
    host = os.environ['POSTGRES_HOST']
    port = os.environ['POSTGRES_PORT']
    return 'postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, db)


def connect_db(params):
    """ Connect to the PostgreSQL database server """
    logging.info('Connecting to the PostgreSQL database...')
    return psycopg2.connect(params)


def create_table(conn):
    cur = conn.cursor()
    logging.info('creatin table ...')
    cur.execute("""CREATE TABLE IF NOT EXISTS events (
        id SERIAL PRIMARY KEY,
        date DATE NOT NULL,
        time VARCHAR NOT NULL,
        location VARCHAR NOT NULL,
        title VARCHAR NOT NULL,
        image_link VARCHAR NOT NULL,
        artists json
    );""")

    conn.commit()
    cur.close()
    logging.info('table created ...')


def insert_data(events, conn):
    logging.info('inserting data into table ....')
    cur = conn.cursor()

    for event in events:
        query = """INSERT INTO events (date, time, location, title, artists, image_link) VALUES (%s, %s, %s, %s, %s, %s)"""
        cur.execute(query, (event.date, event.time, event.location, event.title, json.dumps(event.artists), event.image_link))
    conn.commit()
    cur.close()
    logging.info('data is written ....')
