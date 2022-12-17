from categories.кухни.first.main import parse_first
from categories.кухни.second.main import parse_second
from categories.кухни.third.main import parse_third
from categories.кухни.forth.main import parse_forth, setup


if __name__ == '__main__':
    parse_first()
    parse_second()
    parse_third(setup('https://www.marya.ru/kuhni-sovety/'))
    parse_forth(setup('https://zovrus.ru/article'))


