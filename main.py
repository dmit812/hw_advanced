import json
from hh_parser import *
import requests


if __name__ == '__main__':
    host = 'https://spb.hh.ru/search/vacancy'
    result = []
    count = 0
    while True:
        response = requests.get(url=host, headers=get_headers(), params=get_param(count))
        time.sleep(0.1)
        if count <= 10:
            parse_link(host, result, count)
            count += 1
        else:
            print('На сегодня это все вакансии.')
            break

    with open('vacancy.json', 'w', encoding='utf-8') as v:
        json.dump(result, v, ensure_ascii=False)
