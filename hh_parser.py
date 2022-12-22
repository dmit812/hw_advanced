import re
import time
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers


def get_headers():
    return Headers(browser='chrome', os='win').generate()


def get_param(page_num):
    return {
        'text': 'python',
        'area': [1, 2],
        'page': page_num
    }


def parse_link(host, res_list, page_num):
    comp = {'data-qa': "vacancy-serp__vacancy-employer"}
    address = {'data-qa': "vacancy-serp__vacancy-address"}
    regexp_search = r'.*((D|d)jango).*((F|f)lask).*'
    req = requests.get(url=host, headers=get_headers(), params=get_param(page_num))
    soup = BeautifulSoup(req.text, 'lxml')
    link = soup.find_all('a', class_="serp-item__title")
    name_company = soup.find_all('a', attrs=comp)
    address_company = soup.find_all(attrs=address)
    for i, inf in enumerate(link):
        sal_vac = _salary_vacancy(inf.attrs['href'])
        if re.match(regexp_search, sal_vac[1]):
            res_list.append({
                'title': inf.contents[0],
                'link': inf.attrs['href'],
                'company': name_company[i].text,
                'salary': sal_vac[0],
                'city': address_company[i].text
                })
        time.sleep(0.1)


def _salary_vacancy(url):
    while True:
        req = requests.get(url=url, headers=get_headers())
        attr_description = {'data-qa': "vacancy-description"}
        soup = BeautifulSoup(req.text, 'lxml')
        salary = soup.find("span", class_="bloko-header-section-2 bloko-header-section-2_lite")
        if salary is None:
            time.sleep(0.2)
            continue
        description = soup.find(attrs=attr_description)
        text_salary = salary.text.replace('\xa0', "")
        return [text_salary, description.text]
