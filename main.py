from first.main import parse_first
from second.main import parse_second
from third.main import parse_third
from forth.main import parse_forth, setup


if __name__ == '__main__':
    parse_first()
    parse_second()
    parse_third(setup('https://www.marya.ru/kuhni-sovety/'))
    parse_forth(setup('https://zovrus.ru/article'))


