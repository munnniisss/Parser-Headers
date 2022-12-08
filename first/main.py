import requests
import sqlite3
from bs4 import BeautifulSoup
from pyuser_agent import UA


def check_db(title: str) -> bool:
    conn = sqlite3.connect('db.db')
    q = conn.cursor()

    sql = 'SELECT * FROM titles WHERE title = ?'
    q.execute(sql, (title,))
    data = q.fetchone()

    if data is None:
        sql = 'INSERT INTO titles VALUES(?)'
        q.execute(sql, (title,))
        conn.commit()
        return True
    else:
        return False


def generate_fake_ua() -> UA:
    ua = UA()
    return ua.random


def parse_first():
    status = True
    count = 0

    url = 'https://www.houzz.ru/ideabooks/kuhni'

    while status:

        if count != 0:
            url_result = 'https://www.houzz.ru' + next_page
        else:
            url_result = url

        headers = {
            'User-Agent': generate_fake_ua()
        }

        data = requests.get(url_result, headers)
        soup = BeautifulSoup(data.text, 'lxml')

        titles = [title.text for title in soup.findAll('a', class_='gallery-text__title')]

        for title in titles:
            status = check_db(title)

        try:
            next_page = soup.findAll('a', class_='hz-pagination-link hz-pagination-link--next')[-1]['href']
        except IndexError:
            status = False

        count += 1
