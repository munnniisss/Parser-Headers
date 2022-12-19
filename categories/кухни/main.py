import requests
import sqlite3
from bs4 import BeautifulSoup
from pyuser_agent import UA


def check_by_keywords(string: str) -> bool:
    keywords = ['Вардек']
    for word in keywords:
        if word.lower() in string.lower():
            return False
    return True

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


def setup(url):

    # симитировали get запрос. response - code 200 ()
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    return soup


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


def parse_third(soup: BeautifulSoup):
    home_page_titles = soup.find_all('div', class_='uk-h5 title-target uk-margin-remove-bottom')
    for title in home_page_titles:
        status = check_db(title.text)
        if not status:
            break

    last_page_url = soup.find_all('font', class_='text')[1].find_all('a')[5].get(
        'href')  # получить ссылку на последнюю страницу
    # получить последний символ  строки и сделать его int, тем самым узнаем количество страниц

    list_of_symbol = last_page_url.split('?')  # ['/kuhni-sovety/', 'PAGEN_3=15']
    list_of_pref = list_of_symbol[-1].split('=')  #
    last_page_id = int(list_of_pref[-1])  # 15
    PREF = '?PAGEN_3='
    for i in range(2, last_page_id + 1):
        url = 'https://www.marya.ru' + list_of_symbol[0] + PREF + str(i)
        soup = setup(url)
        next_page_titles = soup.find_all('div', class_='uk-h5 title-target uk-margin-remove-bottom')
        for title in next_page_titles:
            status = check_db(title.text)
            if not status:
                break


def parse_forth(soup: BeautifulSoup):
    titles = soup.find_all('h3', class_='h3')
    for title in titles:
        status = check_db(title.text)
        if not status:
            break