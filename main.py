import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import unicodedata
from pprint import pprint
import lxml
import json


def get_headers():
    return Headers(browser="firefox", os="win").generate()

HOST = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"
SEARCH = f"{HOST}/search/vacancy?text=python&area=1&area=2"

parced_data = []

search_page = requests.get(HOST, headers=get_headers()).text
bs1 = BeautifulSoup(search_page, features="lxml")
vacancy_list = bs1.find_all(class_="serp-item__title")
for vacancy in vacancy_list:
    vacancy_info = {}
    link = vacancy.get("href")
    vacancy_page = requests.get(link, headers=get_headers()).text
    bs2 = BeautifulSoup(vacancy_page, features="lxml")
    vacancy_description = bs2.find("div", {"data-qa": "vacancy-description"}).text
    if 'Django' or 'Flask ' in vacancy_description:
        vacancy_info['link'] = link
        vacancy_title = bs2.find(class_="bloko-header-section-1").text
        vacancy_info['vacancy'] = vacancy_title
        salary = bs2.find(class_="bloko-header-section-2").get_text()
        salary = unicodedata.normalize('NFKD', salary)
        vacancy_info['salary'] = salary
        company = bs2.find(class_="vacancy-company-name").find(class_="bloko-header-section-2_lite").text
        company = unicodedata.normalize('NFKD', company)
        vacancy_info['company'] = company
        city = bs2.find("p", {"data-qa": "vacancy-view-location"})
        if city != None:
            city = city.text
            vacancy_info['city'] = city
        else:
            pass
        parced_data.append(vacancy_info)
    else:
        pass

with open('data.json', 'w', encoding='utf8') as f:
    json.dump(parced_data, f, ensure_ascii=False)
with open('data.json', 'r', encoding='utf8') as f1:
    file = f1.read()
    pprint(file)






