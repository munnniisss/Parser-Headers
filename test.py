# import sqlite3
# import requests
# from bs4 import BeautifulSoup
# from pyuser_agent import UA
#
#
# def generate_fake_ua() -> UA:
#     ua = UA()
#     return ua.random
#
#
# def check_db(title: str) -> bool:
#     conn = sqlite3.connect('db.db')
#     q = conn.cursor()
#
#     sql = 'SELECT * FROM titles WHERE title = ?'
#     q.execute(sql, (title,))
#     data = q.fetchone()
#
#     if data is None:
#         sql = 'INSERT INTO titles VALUES(?)'
#         q.execute(sql, (title,))
#         conn.commit()
#         return True
#     else:
#         return False
#
#
# url = 'https://euronewform.ru/blog'
#
# headers = {
#         'User-Agent': generate_fake_ua()
#     }
#
# data = requests.get(url, headers).text
#
# soup = BeautifulSoup(data, 'lxml')
#
# titles = [title.text for title in soup.findAll('a', class_='g-article__name')]
#
# page_next = soup.findAll('a', class_='g-pagination__item')[-1]
#
# while True:
#     if 'Вперёд' not in page_next.text:
#         break
#
#     current_url = url.replace('/blog', '') + page_next['href']
#     data = requests.get(current_url, headers).text
#     soup = BeautifulSoup(data, 'lxml')
#
#     titles = [title.text for title in soup.findAll('a', class_='g-article__name')]
#
#
#     page_next = soup.findAll('a', class_='g-pagination__item')[-1]
