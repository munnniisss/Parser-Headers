from bs4 import BeautifulSoup
import requests
from first.main import check_db


def setup(url):

    # симитировали get запрос. response - code 200 ()
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    return soup


def parse_forth(soup: BeautifulSoup):
    titles = soup.find_all('h3', class_='h3')
    for title in titles:
        status = check_db(title.text)
        if not status:
            break
