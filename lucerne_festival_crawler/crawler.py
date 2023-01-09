import logging
from typing import List, Tuple
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datetime import datetime, date

BASE_URL = "https://www.lucernefestival.ch"
EVENTS_URL = f"{BASE_URL}/en/program/summer-festival-23"
logging.getLogger().setLevel(logging.INFO)


@dataclass_json
@dataclass
class Event:
    date: date
    time: str
    location: str
    title: str
    artists: List[dict]
    image_link: str


def get_date_and_location(event_soup: BeautifulSoup) -> Tuple[datetime, str]:
    elements = event_soup.find(string='Date and Venue').parent.next_siblings
    elements = [element.strip() for element in elements if not element.name]
    elements = elements[0].split('|')
    date_time_str = f'{elements[0].strip()}{datetime.today().year} {elements[1].strip()}'
    date_time = datetime.strptime(date_time_str, "%a %d.%m.%Y %H.%M")
    location = elements[2].replace("|", "").strip()
    return date_time, location


def get_artists(event_soup: BeautifulSoup) -> List[dict]:
    performer_list = event_soup.find("ul", class_="performers-list")
    artists = []
    for li in performer_list.findAll('li'):
        artist = dict()
        for child in li.children:
            if child.name == 'strong':
                artist['name'] = child.text.strip()
            if child.name == 'span':
                artist['role'] = child.text.strip()
        artists.append(artist)
    return artists


def get_event_objects(events: List[BeautifulSoup]) -> List[Event]:
    event_objects = []
    for event in events:
        event_title = event.find(class_="event-title").text.strip()

        date_time, location = get_date_and_location(event)

        detail_page_link = event.find("a", class_="event-image-link")["href"]
        detail_page_url = f"{BASE_URL}{detail_page_link}"
        detail_page = requests.get(detail_page_url)
        detail_page_soup = BeautifulSoup(detail_page.content, "html.parser")

        image_link = f'{BASE_URL}{detail_page_soup.find("img").attrs["src"]}'
        artists = get_artists(detail_page_soup)

        event_obj = Event(date_time.date(), str(date_time.time()), location, event_title, artists, image_link)
        event_objects.append(event_obj)
    return event_objects


def get_events() -> List[Event]:
    logging.info('Crawling events ...')
    page = requests.get(EVENTS_URL)
    soup = BeautifulSoup(page.content, "html.parser")
    events = soup.find_all(class_="event-item")
    events_list = get_event_objects(events)
    return events_list
