from bs4 import BeautifulSoup
from first.main import check_db
from forth.main import setup


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
