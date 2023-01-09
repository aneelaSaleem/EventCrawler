import mock
import psycopg2

from lucerne_festival_crawler.crawler import get_events
from lucerne_festival_crawler.db_handler import connect_db, get_connection_string_from_env, insert_data, create_table


def test_connect(mocker):
    mocker.patch.object(psycopg2, 'connect')
    connect_db(get_connection_string_from_env())
    psycopg2.connect.assert_called_once()


def test_create_table(mocker):
    conn = mock.MagicMock()
    cur = mock.MagicMock()
    mocker.patch.object(conn, 'cursor', return_value=cur)
    create_table(conn)
    cur.execute.assert_called_once_with("""CREATE TABLE IF NOT EXISTS events (
        id SERIAL PRIMARY KEY,
        date DATE NOT NULL,
        time VARCHAR NOT NULL,
        location VARCHAR NOT NULL,
        title VARCHAR NOT NULL,
        image_link VARCHAR NOT NULL,
        artists json
    );""")
    conn.commit.assert_called_once()
    cur.close.assert_called_once()


def test_insert_data(mocker):
    events = get_events()
    conn = mock.MagicMock()
    cur = mock.MagicMock()
    mocker.patch.object(conn, 'cursor', return_value=cur)
    insert_data(events, conn)
    cur.execute.assert_called()
    assert cur.execute.call_count == len(events)
    conn.commit.assert_called_once()
    cur.close.assert_called_once()
