from bs4 import BeautifulSoup
from unittest.mock import patch

from lucerne_festival_crawler.crawler import get_date_and_location, get_artists, get_event_objects
from datetime import date
import pytest


def test_get_date_and_location():
    event_soup = BeautifulSoup(
        "<html><body><div><strong>Date and Venue</strong><br>Mon 10.05. | 19.30 | KKL Luzern</div></body></html>",
        "html.parser")
    date_time, location = get_date_and_location(event_soup)
    assert date_time.date() == date(2023, 5, 10)
    assert location == "KKL Luzern"


def test_get_date_and_location_invalid_input():
    event_soup = BeautifulSoup(
        "<html><body><div><strong>Date and Venue</strong><br>Mon 10. | 19.30 | KKL Luzern</div></body></html>",
        "html.parser")
    with pytest.raises(ValueError):
        get_date_and_location(event_soup)


def test_get_date_and_location_missing_input():
    event_soup = BeautifulSoup("<html><body>Date and Venue</body></html>", "html.parser")
    with pytest.raises(IndexError):
        get_date_and_location(event_soup)


def test_get_artists():
    event_soup = BeautifulSoup("""<html>
                                    <body>
                                        <ul class="performers-list">
                                            <li><strong>John Smith</strong> <span>vocals</span></li>
                                            <li><strong>Jane Doe</strong> <span>piano</span></li>
                                        </ul>
                                    </body>
                                </html>""", "html.parser")
    artists = get_artists(event_soup)
    assert len(artists) == 2
    assert artists[0]['name'] == "John Smith"
    assert artists[0]['role'] == "vocals"
    assert artists[1]['name'] == "Jane Doe"
    assert artists[1]['role'] == "piano"


def test_get_artists_missing_input():
    event_soup = BeautifulSoup("<html><body><ul class='performers-list'></ul></body></html>", "html.parser")
    artists = get_artists(event_soup)
    assert len(artists) == 0


def test_get_artists_invalid_input():
    event_soup = BeautifulSoup("""<html>
                                    <body>
                                        <ul class="performers-list">
                                            Invalid Artist
                                        </ul>
                                    </body>
                                </html>""", "html.parser")
    artists = get_artists(event_soup)
    assert len(artists) == 0


@patch("lucerne_festival_crawler.crawler.get_artists")
def test_get_event_objects_with_input(mock_artist):
    events = [BeautifulSoup("""<html>
                                <body>
                                    <div class="event-title">Event 1</div>
                                    <div><strong>Date and Venue</strong><br>Mon 10.05. | 19.30 | KKL Luzern</div>
                                    <a class="event-image-link" href="/event1"></a>
                                </body>
                              </html>""", "html.parser"),
              BeautifulSoup("""<html>
                                <body>
                                    <div class="event-title">Event 2</div>
                                    <div><strong>Date and Venue</strong><br>Tue 11.05. | 19.30 | KKL Luzern</div>
                                    <a class="event-image-link" href="/event2"></a>
                                </body>
                              </html>""", "html.parser")]

    event_objects = get_event_objects(events)
    assert len(event_objects) == 2
    assert event_objects[0].title == "Event 1"
    assert event_objects[0].date == date(2023, 5, 10)
    assert event_objects[0].location == "KKL Luzern"
    assert event_objects[1].title == "Event 2"
    assert event_objects[1].date == date(2023, 5, 11)
    assert event_objects[1].location == "KKL Luzern"
