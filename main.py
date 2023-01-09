from lucerne_festival_crawler.db_handler import connect_db, get_connection_string_from_env, create_table, insert_data
from lucerne_festival_crawler.crawler import get_events


if __name__ == '__main__':
    events = get_events()
    params = get_connection_string_from_env()
    conn = connect_db(params)
    create_table(conn)
    insert_data(events, conn)
