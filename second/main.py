import sqlite3
import requests
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


def check_by_keywords(string: str) -> bool:
    keywords = ['Вардек']
    for word in keywords:
        if word.lower() in string.lower():
            return False
    return True


def generate_fake_ua() -> UA:
    ua = UA()
    return ua.random


def parse_second():
    url = 'https://vardek.ru/stati/'

    headers = {
        'User-Agent': generate_fake_ua()
    }

    data = requests.get(url, headers).text

    soup = BeautifulSoup(data, 'lxml')

    count_of_pages = int(soup.findAll('a', class_='pagination__link')[-1].text)

    for page in range(1, count_of_pages + 1):
        current_url = url + f'?PAGEN_2={page}'

        data = requests.get(current_url, headers).text
        soup = BeautifulSoup(data, 'lxml')
        titles = [title.text.strip() for title in soup.findAll('h2', class_='news-list__title')]

        for title in titles:
            if check_by_keywords(title):
                status = check_db(title)
                if not status:
                    break