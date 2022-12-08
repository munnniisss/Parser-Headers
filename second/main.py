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


def generate_fake_ua() -> UA:
    ua = UA()
    return ua.random


def check_by_keywords(string: str) -> bool:
    keywords = ['Мария', 'Марии', 'Marya', 'Марию', '2018', '2019', '2020', '2021', 'Cosmo']
    for word in keywords:
        if word.lower() in string.lower():
            return False
    return True


def parse_second():
    status = True
    count = 1

    url = 'https://www.marya.ru/kuhni-sovety/'

    while status:
        url_result = url + f'?PAGEN_3={count}'

        headers = {
                    'User-Agent': generate_fake_ua()
                }

        data = requests.get(url_result, headers).text
        soup = BeautifulSoup(data, 'lxml')

        headers = soup.findAll('div', class_='uk-h5 title-target uk-margin-remove-bottom')
        headers = [header.text for header in headers]

        for header in headers:
            if check_by_keywords(header):
                status = check_db(header)

        count += 1
